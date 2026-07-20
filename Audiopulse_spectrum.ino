#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

const byte ledPins[6] = {3, 5, 6, 9, 10, 11};

char rxBuffer[64];
byte rxIndex = 0;

uint8_t targetBrightness[6] = {0};
uint8_t currentBrightness[6] = {0};

uint8_t volume = 0;
bool beat = false;
int beatValue = 0;

unsigned long lastOLEDUpdate = 0;
const uint16_t OLED_INTERVAL = 100;

bool receivePacket();
void parsePacket(char *packet);
void updateLEDs();
void drawOLED();
void drawSpectrum();
void drawStatus();

void setup()
{
    Serial.begin(9600);

    for (byte i = 0; i < 6; i++)
    {
        pinMode(ledPins[i], OUTPUT);
        analogWrite(ledPins[i], 0);
    }

    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
    {
        while (true);
    }

    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);

    display.setTextSize(2);
    display.setCursor(12, 14);
    display.println("Audio");

    display.setCursor(12, 38);
    display.println("Pulse");

    display.display();

    delay(1500);

    display.clearDisplay();
    display.display();
}

void loop()
{
    if (receivePacket())
    {
        updateLEDs();
    }

    if (millis() - lastOLEDUpdate >= OLED_INTERVAL)
    {
        lastOLEDUpdate = millis();
        drawOLED();
    }
}

bool receivePacket()
{
    while (Serial.available())
    {
        char c = Serial.read();

        if (c == '\r')
            continue;

        if (c == '\n')
        {
            rxBuffer[rxIndex] = '\0';

            parsePacket(rxBuffer);

            rxIndex = 0;

            return true;
        }

        if (rxIndex < sizeof(rxBuffer) - 1)
        {
            rxBuffer[rxIndex++] = c;
        }
    }

    return false;
}

void parsePacket(char *packet)
{
    int values[6];

    if (sscanf(
            packet,
            "L:%d,%d,%d,%d,%d,%d;V:%hhu;B:%d",
            &values[0],
            &values[1],
            &values[2],
            &values[3],
            &values[4],
            &values[5],
            &volume,
            &beatValue) == 8)
    {
        for (byte i = 0; i < 6; i++)
        {
            targetBrightness[i] = constrain(values[i], 0, 255);
        }

        beat = (beatValue == 1);
    }
}

void updateLEDs()
{
    for (byte i = 0; i < 6; i++)
    {
        int diff = (int)targetBrightness[i] - (int)currentBrightness[i];
        currentBrightness[i] += diff / 4;
        analogWrite(ledPins[i], currentBrightness[i]);
    }
}

void drawStatus()
{
    display.setTextSize(1);

    display.setCursor(0, 0);
    display.print("AudioPulse");

    display.setCursor(0, 10);
    display.print("VOL:");
    display.print(volume);
    display.print("%");

    display.setCursor(78, 10);

    if (beat)
        display.print("BEAT");
    else
        display.print("----");
}

void drawSpectrum()
{
    const byte baseY = 63;
    const byte barWidth = 16;
    const byte gap = 4;
    const byte maxHeight = 44;

    for (byte i = 0; i < 6; i++)
    {
        int h = map(currentBrightness[i], 0, 255, 0, maxHeight);

        int x = i * (barWidth + gap);

        display.drawRect(x, baseY - maxHeight, barWidth, maxHeight, SSD1306_WHITE);

        if (h > 0)
        {
            display.fillRect(
                x + 2,
                baseY - h,
                barWidth - 4,
                h,
                SSD1306_WHITE
            );
        }
    }
}

void drawOLED()
{
    display.clearDisplay();

    drawStatus();

    drawSpectrum();

    if (beat)
    {
        display.fillCircle(122, 4, 3, SSD1306_WHITE);
    }
    else
    {
        display.drawCircle(122, 4, 3, SSD1306_WHITE);
    }

    display.display();
}