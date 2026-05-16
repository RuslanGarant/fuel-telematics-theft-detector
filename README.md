# IoT Fuel Telematics & Theft Detection Module

This repository contains an open-source data analytics module designed for commercial fleet management and IoT telematics platforms. It processes real-time data streams from Fuel Level Sensors (FLS) to filter out fuel sloshing noises and automatically identify fuel theft events.

## Technical Methodology
Fuel level sensors in commercial heavy trucks experience intense signal noise ("sloshing") due to vehicle acceleration, braking, and rough terrain. 

This software applies a Moving Average Filter to stabilize raw sensor readings. It then runs an anomaly detection logic that monitors fuel volume drops specifically during the **Ignition OFF** state to isolate fuel draining/theft from normal engine consumption.

## Architecture & Logic Flow
```mermaid
graph TD
    A[Receive Raw FLS Telematics Data] --> B[Apply Moving Average Filtering]
    B --> C[Calculate Fuel Level Delta]
    C --> D{Is Ignition ON?}
    D -->|Yes| E[Check against Normal Consumption Rates]
    E --> A
    D -->|No| F{Fuel Drop >= Threshold?}
    F -->|No / Stable| G[System Normal State]
    G --> A
    F -->|Yes / Anomaly| H[Trigger Fuel Theft Alert]
    H --> I[Generate Telematics Alarm Payload for Fleet Management Server]
