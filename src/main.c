
#include "font.h"
#include <string.h> // for memset
#include "ssd1306.h"
#include "hardware/i2c.h"
#include "pico/stdlib.h"
#include <stdio.h> // Add include for printf and scanf
#include "pico/binary_info.h"
#include "hardware/gpio.h"
#include "hardware/spi.h"
#include "hardware/adc.h"
#include "hardware/clocks.h"
#include "hardware/uart.h"
#include "hardware/irq.h" // for the interrupt system

#define CHAR_WIDTH 5
#define CHAR_HEIGHT 8
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define UART_ID uart0
#define BAUD_RATE 115200
#define DATA_BITS 8
#define STOP_BITS 1
#define PARITY UART_PARITY_NONE

#define UART_TX_PIN 0 // We are using pins 0 and 1, but see the GPIO function select table in the
#define UART_RX_PIN 1 // datasheet for information on which other pins can be used.
static int chars_rxed = 0;

volatile int x = 0;
unsigned char set = 5;
unsigned char SSD1306_ADDRESS = 0b0111100; // 7bit i2c address
unsigned char ssd1306_buffer[513];         // 128x32/8. Every bit is a pixel except first byte

// // Function to initialize I2C communication
void init_i2c()
{
  i2c_init(i2c_default, 100 * 1000); // Initialize I2C at 100kHz
  gpio_set_function(PICO_DEFAULT_I2C_SDA_PIN, GPIO_FUNC_I2C);
  gpio_set_function(PICO_DEFAULT_I2C_SCL_PIN, GPIO_FUNC_I2C);
  gpio_pull_up(PICO_DEFAULT_I2C_SDA_PIN);
  gpio_pull_up(PICO_DEFAULT_I2C_SCL_PIN); // Enable pull-up on SCL IODIR 1 = input
}

void ssd1306_setup()
{
  // first byte in ssd1306_buffer is a command
  ssd1306_buffer[0] = 0x40;
  // give a little delay for the ssd1306 to power up
  //_CP0_SET_COUNT(0);
  // while (_CP0_GET_COUNT() < 48000000 / 2 / 50) {
  //}
  sleep_ms(20);
  ssd1306_command(SSD1306_DISPLAYOFF);
  ssd1306_command(SSD1306_SETDISPLAYCLOCKDIV);
  ssd1306_command(0x80);
  ssd1306_command(SSD1306_SETMULTIPLEX);
  ssd1306_command(0x1F); // height-1 = 31
  ssd1306_command(SSD1306_SETDISPLAYOFFSET);
  ssd1306_command(0x0);
  ssd1306_command(SSD1306_SETSTARTLINE);
  ssd1306_command(SSD1306_CHARGEPUMP);
  ssd1306_command(0x14);
  ssd1306_command(SSD1306_MEMORYMODE);
  ssd1306_command(0x00);
  ssd1306_command(SSD1306_SEGREMAP | 0x1);
  ssd1306_command(SSD1306_COMSCANDEC);
  ssd1306_command(SSD1306_SETCOMPINS);
  ssd1306_command(0x02);
  ssd1306_command(SSD1306_SETCONTRAST);
  ssd1306_command(0x8F);
  ssd1306_command(SSD1306_SETPRECHARGE);
  ssd1306_command(0xF1);
  ssd1306_command(SSD1306_SETVCOMDETECT);
  ssd1306_command(0x40);
  ssd1306_command(SSD1306_DISPLAYON);
  ssd1306_clear();
  ssd1306_update();
}

// send a command instruction (not pixel data)
void ssd1306_command(unsigned char c)
{
  uint8_t buf[2];
  buf[0] = 0x00;
  buf[1] = c;
  i2c_write_blocking(i2c_default, SSD1306_ADDRESS, buf, 2, false);
}

// update every pixel on the screen
void ssd1306_update()
{
  ssd1306_command(SSD1306_PAGEADDR);
  ssd1306_command(0);
  ssd1306_command(0xFF);
  ssd1306_command(SSD1306_COLUMNADDR);
  ssd1306_command(0);
  ssd1306_command(128 - 1); // Width

  unsigned short count = 512;          // WIDTH * ((HEIGHT + 7) / 8)
  unsigned char *ptr = ssd1306_buffer; // first address of the pixel buffer
  /*
  i2c_master_start();
  i2c_master_send(ssd1306_write);
  i2c_master_send(0x40); // send pixel data
  // send every pixel
  while (count--) {
      i2c_master_send(*ptr++);
  }
  i2c_master_stop();
  */

  i2c_write_blocking(i2c_default, SSD1306_ADDRESS, ptr, 513, false);
}

// zero every pixel value
void ssd1306_clear()
{
  memset(ssd1306_buffer, 0, 512); // make every bit a 0, memset in string.h
  ssd1306_buffer[0] = 0x40;       // first byte is part of command
}

void drawChar(int x, int y, char character)
{
  if (character < 32 || character > 126)
  {
    // Character out of range
    return;
  }

  int charIndex = character - 32; // ASCII starts from 32
  const char *charData = ASCII[charIndex];

  for (int j = 0; j < CHAR_WIDTH; ++j)
  {
    for (int i = 0; i < CHAR_HEIGHT; ++i)
    {
      if (charData[j] & (1 << (CHAR_HEIGHT - i - 1)))
      {
        // Draw pixel at position (x + j, y + i)
        ssd1306_drawPixel(x + j, y - i, 1); // Set pixel to on
      }
      else
      {
        ssd1306_drawPixel(x + j, y - i, 0); // Set pixel to off
      }
    }
  }
}

// set a pixel value. Call update() to push to the display)
// 1 = on  |   0 = off (takes the x and y location)
void ssd1306_drawPixel(unsigned char x, unsigned char y, unsigned char color)
{
  if ((x < 0) || (x >= 128) || (y < 0) || (y >= 32))
  {
    // Character out of range
    return;
  }

  if (color == 1)
  {
    ssd1306_buffer[1 + x + (y / 8) * 128] |= (1 << (y & 7));
  }
  else
  {
    ssd1306_buffer[1 + x + (y / 8) * 128] &= ~(1 << (y & 7));
  }
}

// RX interrupt handler
void on_uart_rx()
{
  while (uart_is_readable(UART_ID)) // which uart generated
  {
    uint8_t ch = uart_getc(UART_ID); // read the letter gotten
    /* if (ch == '\r') {
        drawString(m,0,0)
        i = 0;
    }*/

    // if (ch == '\n') { x = 0}
    // else {input drawChar(ch,x,y) function}

    x = x + 5;
    // Can we send it back?
    if (uart_is_writable(UART_ID))
    {
      // Change it slightly first!

      uart_putc(UART_ID, ch);
    }
    chars_rxed++;

    // Draw character on SSD1306 display
    drawChar(x, SCREEN_HEIGHT / 2, ch);
    ssd1306_update();
  }
}

int main()
{
  stdio_init_all(); // Initialize UART for input/output

  init_i2c();
  ssd1306_setup(); // Initialize SSD1306 display

  // Initialize ADC
  adc_init();
  adc_gpio_init(26);   // Use GPIO26 as ADC pin
  adc_select_input(0); // Select ADC0 as input

  uart_init(UART_ID, 2400);

  gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART); // Set the TX and RX pins by using the function select on the GPIO
  gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART); // Set datasheet for more information on function select
  // Actually, we want a different speed
  // The call will return the actual baud rate selected, which will be as close as
  // possible to that requested
  int __unused actual = uart_set_baudrate(UART_ID, BAUD_RATE); // checks the baud rate and then sends back the actual baud rate

  // Set UART flow control CTS/RTS, we don't want these, so turn them off
  uart_set_hw_flow(UART_ID, false, false);

  // Set our data format
  // (want to send 8 bits of data. one stop bit with no parity, )
  uart_set_format(UART_ID, DATA_BITS, STOP_BITS, PARITY);

  uart_set_fifo_enabled(UART_ID, false); // Turn off FIFO's - we want to do this character by character

  // Set up a RX interrupt
  // We need to set up the handler first
  // Select correct interrupt for the UART we are using
  int UART_IRQ = UART_ID == uart0 ? UART0_IRQ : UART1_IRQ;

  // And set up and enable the interrupt handlers
  irq_set_exclusive_handler(UART_IRQ, on_uart_rx); // calls on_uart_rx when you receive a letter
  irq_set_enabled(UART_IRQ, true);

  // Now enable the UART to send interrupts - RX only
  uart_set_irq_enables(UART_ID, true, false);

  // Send a basic string out, and then run a loop and wait for RX interrupts
  // The handler will count them, but also reflect the incoming data back with a slight change!
  uart_puts(UART_ID, "\nHello, uart interrupts\n");

  char input[100] = "Hello World"; // Default string
  char fps_str[20];

  while (1)
    tight_loop_contents();
}