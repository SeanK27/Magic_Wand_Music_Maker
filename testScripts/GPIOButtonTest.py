import gpiozero

button = gpiozero.Button(36)

while True:
    if button.is_active:
        print("pressed")