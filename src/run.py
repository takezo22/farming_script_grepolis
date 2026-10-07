from fonctionsgrepo import *


login()

time.sleep(5)

while True:
    collecte(freq_commerce*60)
    delay()
    commerce()
    delay()
    construction()
    delay()