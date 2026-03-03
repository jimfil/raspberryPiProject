**RQ1: Is a PIR sensor active or passive? Contact or no-contact? Explain in your own words.**
Ans: Passive, no-contact because it detects the infrared radiation emitted by objects, rather than emitting its own signal.

**RQ2: What is the output range/representation of this sensor?**
Ans: The HC-SR501 sensor that we used in this lab has an adjustable detection range from ~3m to ~7m, and and adjustable output high time from ~3s to ~300s. The output is a digital signal, which is high when the sensor detects motion and low when it does not.

**RQ3: If TIME is set to 300s, what wrong assumption might your software make about “continuous motion”?**
Ans: When a small movement occurs even for 1 second, the sensor will assume that movements exists for 300s, which is not true. 

**RQ4: Why does warm-up time matter in real deployments?**
Ans: In real deployments, the sensor must be stable without providing false triggers so adjusting to the rooms IR levels is critical.

**RQ5: Explain a realistic bug that happens when a team mixes BCM and BOARD numbering.**
Ans: The most common bug is that the code will not work as expected, because the pins are not connected to the correct pins. For example, if a team member uses BCM numbering when the code is written in BOARD numbering, the code will not work as expected.

**RQ6: Fill in the wiring table for your setup (use your actual pins).**
Ans: 