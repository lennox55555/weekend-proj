# Weather Data Pipeline

This project implements a serverless weather data pipeline that fetches, processes, and combines weather data from multiple cities using AWS services.

## Functional Pipeline Implementation

The pipeline consists of the following components:

1. **Data Collection**: Fetches weather data for New York City and Los Angeles from the OpenWeather API
2. **Data Storage**: Stores the raw data in an S3 bucket with organized directory structure (by city, date, and hour)
3. **Data Combination**: Combines the data from both cities into a consolidated output
4. **Orchestration**: Uses AWS Step Functions to coordinate the workflow

The pipeline consists of three Lambda functions:
- `fetch_nyc_weather.py`: Retrieves NYC weather data
- `fetch_la_weather.py`: Retrieves LA weather data 
- `combine_weather.py`: Combines data from both sources

### Error Handling Approach

The pipeline implements robust error handling:
- Using `.get()` with default values when extracting data from JSON responses
- Using `.raise_for_status()` to handle HTTP errors in the API calls
- Configuring environment variables for flexible configuration
- Proper exception handling in S3 operations

## Architecture Documentation

### AWS Services Used

1. **AWS Lambda Functions**: Three stateless functions that each perform a specific task
2. **AWS S3**: Central storage for data with organized partitioning by city, date, and hour
3. **AWS Step Functions**: Orchestration layer that defines workflow execution order
4. **AWS EventBridge**: Triggers the state machine execution on a scheduled basis
5. **AWS IAM**: Proper permission controls for service interactions

### Workflow

The state machine definition shows a sequential workflow:
1. Start with "FetchNYC" - retrieves weather data for New York City
2. Move to "FetchLA" - retrieves weather data for Los Angeles
3. Finish with "Combine" - combines the data from both cities into a single file

Each Lambda function writes its output to S3, and the final combined data is stored in a structured format for easy access and analysis.

## Monitoring Dashboard

The implementation leverages AWS's built-in monitoring capabilities:

- **Lambda Monitoring**: Execution metrics, duration, and error rates for each function
- **Step Functions Dashboard**: Visual workflow tracking with execution status and history
- **CloudWatch Logs**: Detailed logging for debugging and auditing
- **CloudWatch Metrics**: Performance monitoring and alerting

These monitoring tools provide visibility into the pipeline's operation, making it easy to identify and resolve issues.

## Technical Writeup

### Fallbacks and Error Handling

The application implements several fallback mechanisms:
- Using `.get()` with default values for safely extracting data from API responses
- Defensive programming with empty defaults for missing data
- Proper HTTP error handling for API calls
- Environment variable defaults for configuration flexibility

### State Machine as Orchestration

Step Functions provide several advantages as an orchestration layer:
- Clear workflow definition in JSON format
- Sequential execution of Lambda functions
- Automatic retry and error handling
- Visual representation of the workflow
- Separation of concerns between data fetching and processing

### Security Considerations

The implementation follows security best practices:
- IAM roles with principle of least privilege
- Secret management for API keys through environment variables
- Proper trust relationships between services
- S3 bucket policies for data protection

### Data Organization

Data is organized in a structured way:
- S3 paths follow a clear pattern: `raw/<city>/<date>/<hour>.csv`
- Combined data follows a similar pattern: `raw/combined/<date>/<hour>.csv`
- Consistent CSV formatting across all files
- Clear separation between raw and combined data

This serverless architecture provides a scalable, maintainable data pipeline that can be easily extended to include additional cities or data sources.