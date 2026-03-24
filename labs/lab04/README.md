# Section A: Runbook (How to run our code)


*(Add instructions on how to build and run the pipeline here)*

## Section B: Report


**RQ1: What base image did you use and why?**

Ans:

**RQ2: How many layers does your Dockerfile create? Which instructions produce new layers?**
 
Ans:

**RQ3: What is the size of your built image?**

Ans:

**RQ4: Why do we copy requirements.txt and install dependencies before copying the rest of the code? What would happen if we reversed the order?**

Ans:

**RQ5: What does --device /dev/gpiomem do and why is it needed?**

Ans:

**RQ6: What happens to the JSONL output if you run the container without a volume mount (-v)?**

Ans:

**RQ7: Did the pipeline behave the same inside Docker as it did running directly on the Pi in Lab 03? Any differences?**

Ans:

**RQ8: What happened when you set --memory=32m? Does this work on the PI? Why yes, why not?**

Ans: 

**RQ9: Why are resource limits important on edge devices in general?**

Ans: 

**RQ10: What is the advantage of writing a docker-compose.yml instead of using docker run with flags?**

Ans: 

**RQ11: What is the difference between a bind mount (-v $(pwd)/output:/data) and a named volume (pipeline-data:/data)?**

Ans: 

**RQ12: What does restart: unless-stopped do and why does it matter for an edge device?**

Ans: 
**RQ13: What does a virtual environment isolate, and what does it not isolate?**

Ans: 

**RQ14: Give one concrete example where a requirements.txt and a venv would not be enough to reproduce your Lab 03 setup on a different machine.**

Ans: 

**RQ15: Give one scenario where a virtual environment is perhaps a better choice than Docker.**

Ans: 

**RQ16: In the context of the Smart Wastebin project, which approach (venv or Docker) would you prefer to use for a final deployment, and why?**

Ans: 
