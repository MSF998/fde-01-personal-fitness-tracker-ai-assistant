# Web Based Fitness Tracker

## Checklist

- [x] Think in terms of the user
- [x] Which features can be classified as primary or secondary
- [] Expand the hidden flow. Be as technical as possible

## User Actions

1. As a user, I want to set my goals
2. As a user, I want to select predifined workout routines
3. As a user, I want to schedule workouts
4. As a user, I want to mark workouts as completed
5. As a user, I want to see how much I have accomplished (walking, running, swimming, workout)
6. As a user, I want to see my calories, heart rate chart, total calories burnt for the day
7. As a user, I want to store my physical details such as height, weight, age
8. As a user, I want to get personal recommendations based on my activity

## Features

1. Workout Logging
   - Record exercises, sets, reps, weight, duration, or distance
   - View workout history
2. Progress Dashboard
   - Visualize progress with charts (e.g., weight lifted, workouts completed, body weight).
   - Track personal records and consistency.
3. Goals and streaks
   - Set fitness goals
   - Display daily/weekly streaks and goal completion
4. User Profile
   - Store height, weight, age, activity level, and fitness preferences.
   - Calculate BMI and estimate calorie needs.
5. Workout Plans
   - Create or select predefined workout routines
   - Schedule workouts and mark them as completed
6. Personal Recommendations
   - Get AI powered personal recommendations

## Feature Classification (primary/secondary)

### Primary Services

- Workout Logging
- Progress Dashboard
- User Profile

### Secondary Services

- Goals and streaks
- Workout Plans
- Personal Recommendations

## Hidden Flow

1. Workout Logging
   - recieve workout request
   - validate the request payload
   - verify if the excercise IDs exists
   - validate workout metrics (e.g., reps > 0, weight ≥ 0, duration > 0)
   - create a new workout session
   - save workout metadata (date, start time, end time, workout type)
   - save each excercise in the workout
   - save all sets associated with each excercise
   - calculate workout statistics (total volume, total sets, duration, calories if applicable)
   - update user progress (streak, total workouts, personal records)
   - commit the transaction
   - return workout ID and summary

2. Progress Dashboard
   1. Frontend
      - User opens the Progress Dashboard.
      - Read the selected time range (Week/Month/Year/Custom).
      - Read filter preferences (workout type, exercise, muscle group).
      - Check if cached dashboard data exists.
      - Display loading state.
      - Request dashboard data from the backend.
      - Receive progress metrics.
      - Transform data into chart-friendly format.
      - Render summary cards (total workouts, streak, volume, PRs).
      - Render charts (workout frequency, weight progression, volume trend).
      - Handle empty state if no workouts exist.
      - Handle API errors with retry option.
      - Cache the response for faster reloads
   2. API Layer
      - Receive dashboard request (user ID, date range, filters).
      - Authenticate and authorize the user.
      - Validate request parameters.
      - Read workout sessions from the database.
      - Read exercise and set data.
      - Aggregate workout statistics.
      - Calculate total workouts.
      - Calculate total workout duration.
      - Calculate total training volume.
      - Calculate workout streak.
      - Identify personal records.
      - Generate chart datasets (daily/weekly/monthly trends).
      - Compute comparison with previous period (optional).
      - Format the response DTO.
      - Return dashboard data to the frontend
