# Lab 13 - LLMOps

"This lab will cover building LLM-based systems, including efficient LLM inference, enabling tool usage, and securing them with guardrails."

## Hardware constraints
CPU-only machine, 16GB RAM
Decisions: 
- smaller model: Qwen3-0.6B
- deleted "bitsandbytes>=0.49.1" from the pyproject.toml file

## vLLM inference:
after installing the venv I'm using: 
```
vllm serve Qwen/Qwen3-0.6B --port 8000 --max-model-len 2048
``` 
for the hardware constraints mentioned.

That didn't work..
```
raise RuntimeError(
RuntimeError: Failed to infer device type, please set the environment variable `VLLM_LOGGING_LEVEL=DEBUG` to turn on verbose logging to help debug the issue.
```

So I'll use a cloud-hosted LLM - tried OpenAI API but it needs billing to be set up. I'll use Gemini API.

## Exercise 1
I unfortunately cannot run it without the GPU present and vLLM not working (or at least not quickly/cost-free enough)

## Tool usage
Implemented manual tool calling - the first prompt that goes to the llm is the user's prompt combined with instructions about tool handling. The LLM returns an answer and it is checked if it contains the json format needed for the tools. If so - LLM has decided to use a tool. The tool is called and it's result is combined with the original prompt and sent to the LLM agin for the final answer. Both csv and parquet loading worked when tested.

The implementation can be found in `exercise_2_manual_tools.py`.

**Result:**
```
--- LLM RESPONSE (step 1) ---
{
"tool_name": "read_remote_parquet",
"arguments": {
    "url": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet",
    "n_rows": 5
}
}

--- TOOL OUTPUT ---
VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount,congestion_surcharge,Airport_fee
2,2024-01-01T00:57:55.000000000,2024-01-01T01:17:43.000000000,1,1.72,1,N,186,79,2,17.7,1.0,0.5,0.0,0.0,1.0,22.7,2.5,0.0
1,2024-01-01T00:03:00.000000000,2024-01-01T00:09:36.000000000,1,1.8,1,N,140,236,1,10.0,3.5,0.5,3.75,0.0,1.0,18.75,2.5,0.0
1,2024-01-01T00:17:06.000000000,2024-01-01T00:35:01.000000000,1,4.7,1,N,236,79,1,23.3,3.5,0.5,3.0,0.0,1.0,31.3,2.5,0.0
1,2024-01-01T00:36:38.000000000,2024-01-01T00:44:56.000000000,1,1.4,1,N,79,211,1,10.0,3.5,0.5,2.0,0.0,1.0,17.0,2.5,0.0
1,2024-01-01T00:46:51.000000000,2024-01-01T00:52:57.000000000,1,0.8,1,N,211,148,1,7.9,3.5,0.5,3.2,0.0,1.0,16.1,2.5,0.0

USER PROMPT:

The dataset is available at https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet. Can you answer these questions: 
1. What does the dataset seem to represent? 
2. What columns does it contain and of what type? 
3. What analysis could I run on the full dataset?

FINAL ANSWER:

Based on the sample data and the source URL, here are the answers to your questions:

### 1. What does the dataset seem to represent?
This dataset represents **New York City Yellow Taxi trip records** for January 2024. It is part of the official data released by the NYC Taxi and Limousine Commission (TLC). It tracks individual taxi trips, including when and where they started and ended, the distance traveled, the number of passengers, and a detailed breakdown of the fares and fees charged.

### 2. What columns does it contain and of what type?
Based on the provided sample, here are the columns and their inferred data types:

*   **VendorID:** Integer (Categorical ID for the taxi provider)
*   **tpep_pickup_datetime:** Datetime (The start time of the trip)
*   **tpep_dropoff_datetime:** Datetime (The end time of the trip)
*   **passenger_count:** Integer (Number of passengers)
*   **trip_distance:** Float (Distance in miles)
*   **RatecodeID:** Integer (Categorical ID for the rate type, e.g., Standard, JFK, Newark)
*   **store_and_fwd_flag:** String/Boolean (Y/N flag indicating if the record was stored in vehicle memory before sending)
*   **PULocationID:** Integer (TLC Taxi Zone ID for pickup)
*   **DOLocationID:** Integer (TLC Taxi Zone ID for drop-off)
*   **payment_type:** Integer (Categorical ID for how the passenger paid, e.g., Credit Card, Cash)
*   **fare_amount:** Float (The time-and-distance fare)
*   **extra:** Float (Miscellaneous extras and surcharges)
*   **mta_tax:** Float (MTA tax)
*   **tip_amount:** Float (Credit card tips; cash tips are typically not included)
*   **tolls_amount:** Float (Total price of tolls)
*   **improvement_surcharge:** Float (Surcharge for accessible taxicabs)
*   **total_amount:** Float (The total cost charged to the passenger)
*   **congestion_surcharge:** Float (Surcharge for trips in high-traffic areas)
*   **Airport_fee:** Float (Fees for airport pickups/drop-offs)

### 3. What analysis could I run on the full dataset?
With the full version of this dataset (which likely contains millions of rows), you could perform several types of analysis:

*   **Temporal Trends:** Identify the busiest times of day or days of the week. You could determine when the "rush hour" for taxis occurs and how demand fluctuates on weekends vs. weekdays.
*   **Geospatial Mapping:** Using the Location IDs, you can identify the most popular pickup and drop-off neighborhoods (e.g., seeing which areas have the highest demand for trips to the airport).
*   **Revenue Analysis:** Calculate the average fare or tip percentage. You could also analyze which routes or times of day result in the highest tips for drivers.
*   **Trip Efficiency:** By subtracting the pickup time from the drop-off time, you can calculate the duration of trips. Comparing duration to distance would allow you to analyze traffic congestion patterns across the city.
*   **Predictive Modeling:** You could build a machine learning model to predict the `total_amount` or `tip_amount` based on the pickup location, time of day, and trip distance.
```

## Exercise 3 - Model Context Protocol (MCP)
Implemented the MCP server in `exercise_3_mcp_date_server.py`. 
![alt text](image.png)
MCP improves over the manual approach by shifting tool definitions from the client to the server, allowing for automatic tool discovery.

## Exercise 4 - Visualisation MPC server
Implemented the plotting tool in the visualisation MCP server
![alt text](image-1.png)

Generated sample plot:
![](sample_plot.png)

## Exercise 5 - Guardrails
Signed up on Guardrails AI, generated an API key, configured it using `guardrails configure` and installed the restrict to topic and detect jailbreak guardrails:

```
guardrails hub install hub://tryolabs/restricttotopic
guardrails hub install hub://guardrails/detect_jailbreak
```
Then it was a struggle, nothing seemed to work, because the RestrictToTopic guardrail kept trying to use a ChatGPT API key. From the docs (https://github.com/tryolabs/restricttotopic) it turned out that it uses an llm to judge whether the topic is aligned with the one specified, and that llm was automatically one that required a global variable API key. What fixed this was passing a function calling ollama to `llm_callable` to use the model from ollama instead.

It turns out it's not really easy to get a non-fish response, which proves that guardrails are a good security feature.

**The output:**

```
VALID PROMPT (should pass)
Eating fish is an essential part of human survival and a testament to our connection with the ocean. Fish provide vital nutrients, such as protein and omega-3 fatty acids, that are crucial for growth, cognitive function, and overall well-being. From a fishing fanatic’s perspective, the act of capturing and consuming fish is not just a culinary choice but a connection to the natural world and the ecosystems we support. Every piece of fish we eat also symbolizes the delicate balance between humans and the ocean, reminding us of our responsibility to preserve marine life. And yes, as a fisherman, I find joy in the simple act of catching something that nourishes both body and mind.

OFF-TOPIC PROMPT (should be blocked by topic restriction)
Sorry, I can only talk about fishing-related topics.

OFF-TOPIC PROMPT (should be blocked by topic restriction)
The brain, much like the ocean, is a vast network of neurons and neural pathways that perceive, adapt, and process information for survival. Just as fish navigate currents, the brain processes sensory inputs, makes decisions, and learns to adapt in real-time. Here's how the brain works from an enthusiast’s perspective:  

1. **Sensory Perception**: The brain’s sensory receptors (like eyes, ears, and skin) detect environmental changes—sound, light, and movement. This mirrors the fish’s sense of water, which uses light and movement to find food and avoid dangers.  

2. **Learning and Decision-Making**: The brain’s learning mechanisms (like memory and problem-solving) function similarly to how a fish learns to catch prey. Just as a fish studies fishhooks, the brain stores and uses past experiences to guide future actions.  

3. **Adaptability**: The brain’s plasticity is crucial, much like how a fish adapts to new environments or techniques. Whether it’s a new fishing tackle or a new technique, the brain refines itself.  

4. **Nervous System**: The brain relies on the nervous system for communication, a system that works just as a fish communicates with its surroundings.  

In essence, the brain is not just a body part—it's an organ that thrives in complexity, just like the ocean. From the fish's journey to the brain's intricate processes, every function is a testament to life's adaptability and intelligence.
```