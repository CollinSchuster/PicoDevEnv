#include "pico/stdlib.h"
#include "hardware/pwm.h"
#include "pico/time.h"
#include "hardware/irq.h"

#define LEDPin 19                  // the built-in LED on the Pico
#define SERVO_MIN_PULSE_WIDTH 500  // in microseconds
#define SERVO_MAX_PULSE_WIDTH 2500 // in microseconds

float map(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void initializePWM()
{
  gpio_set_function(LEDPin, GPIO_FUNC_PWM);       // Set the LED Pin to be PWM
  uint slice_num = pwm_gpio_to_slice_num(LEDPin); // Get PWM slice number
  float div = 40;                                 // must be between 1-255 for 50Hz (40)
  pwm_set_clkdiv(slice_num, div);                 // divider
  uint16_t wrap = 62500;                          // when to rollover, must be less than 65535
  pwm_set_wrap(slice_num, wrap);
  pwm_set_enabled(slice_num, true); // turn on the PWM
}

void setServoAngle(float angle)
{
  uint slice_num = pwm_gpio_to_slice_num(LEDPin); // Get PWM slice number
  uint16_t pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE_WIDTH, SERVO_MAX_PULSE_WIDTH);
  pwm_set_gpio_level(LEDPin, pulse_width);
}

int main()
{
  stdio_init_all();
  initializePWM();

  float angle = 0;
  float step = 4;                 // degrees to increment per step
  uint32_t step_delay_us = 10000; // delay in microseconds between steps (10ms)

  while (true)
  {
    setServoAngle(angle);
    angle += step;
    if (angle >= 720 || angle <= 0)
    {
      step *= -1; // reverse direction when reaching limits
    }
    sleep_us(step_delay_us);
  }

  return 0;
}
