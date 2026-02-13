# MongoDB Data Interaction Guide

**AI Job Hunt Backend**

This document describes how to safely interact with the MongoDB database
used by the AI Job Hunt backend.\
It is intended for the ML and data ingestion team who need to
ingest, update, or analyze data in collections such as:

-   `users`
-   `jobs`
-   `job_matches`
-   `saved_searches`
-   `user_job_interactions`
-   `user_stats`

------------------------------------------------------------------------

# Database Overview

**Production Database**

    aijobhunt_db

**Test Database**

    aijobhunt_db_test

All collections use MongoDB `ObjectId` references for relationships.

------------------------------------------------------------------------

# Entity Relationships

    User (1) ──── (M) JobMatches ──── (1) Job
    User (1) ──── (M) UserJobInteractions ──── (1) Job
    User (1) ──── (M) SavedSearches
    User (1) ──── (1) UserStats

------------------------------------------------------------------------

# Collection Schemas & Usage

## users

Stores registered user accounts and profile information.

### Schema

``` json
{
  "_id": ObjectId,
  "email": String (unique),
  "name": String,
  "preferences": {
     "desired_locations": Array<String>,
     "target_roles": Array<String>,
     "skills": Array<String>,
     "experience_level": String,
     "salary_min": Number,
     "salary_max": Number
  }
}
```

### Indexes

-   **Unique:** `_id`
-   **Unique:** `email`

### Notes

-   Emails must be unique.
-   Passwords must be securely hashed before insertion.
-   `preferences` and `credentials` are used by ML for match generation.

## CRUD Examples

### Create

``` python
# Create simple user profile
payload = {
    "name": "John Doe",
    "email": "john@test.com"
}

response = await client.post("/users/", json=payload)

# Create user profile with preferences
payload = {
    "name": "Pref User",
    "email": "pref@test.com",
    "preferences": {
        "desired_locations": ["NYC", "SF"],
        "target_roles": ["ML Engineer"],
        "skills": ["Python", "FastAPI"],
        "experience_level": "mid",
        "salary_min": 90000,
        "salary_max": 130000,
    },
}

response = await client.post("/users/", json=payload)
```

### Read

``` python
# Get all users
response = await client.get("/users/")

# Get one user by user ID
response = await client.get(f"/users/{user_id}")
```

### Update

``` python
# Update simple user profile
update = await client.put(
    f"/users/{user_id}",
    json={"name": "New Name"}
)

# Partial update user profile preferences
patch = await client.patch(
    f"/users/{user_id}",
    json={
        "preferences": {
            "salary_min": 80000,
            "salary_max": 120000,
        }
    },
)
```

### Delete

``` python
# Delete one user
delete = await client.delete(f"/users/{user_id}")

"""NOTE: Deleting a user with cause a cascading delete on: UserStats, SavedSearches, UserJobInteractions, JobMatches"""
```
------------------------------------------------------------------------

## jobs

Stores job postings ingested from external sources.

### Schema

``` json
{
  "_id": ObjectId,
  "external_id": String (unique),
  "title": String,
  "company": String,
  "description": String,
  "location": String,
  "remote_type": String,
  "skills_required": Array<String>,
  "posted_date": ISODate,
  "source_url": String,
  "source_platform": String,
  "salary_range": {
     "min": Number,
     "max": Number,
     "currency": String
  },
  "ml_features": {
     "processed_text": String,
     "keyword_vector": Array<Number>
  }
}
```

### Indexes

-   **Unique:** `_id`
-   **Unique:** `external_id`

### Notes

-   `external_id` prevents duplicate ingestion from external APIs.
-   `skills` is used for match scoring.
-   Soft deletes should toggle `is_active` instead of removing
    documents.

## CRUD Examples

### Create

``` python
payload = {
    "external_id": "job-123",
    "title": "Research Scientist",
    "company": "OpenAI Labs",
    "description": "Work on cutting-edge research.",
    "location": "San Francisco",
    "remote_type": "hybrid",
    "skills_required": ["Statistics", "Python"],
    "source_url": "https://example.com/job/123",
    "source_platform": "LinkedIn",
    "salary_range": {
        "min": 140000,
        "max": 200000,
        "currency": "USD",
    },
    "ml_features": {
        "processed_text": "research scientist statistics python",
        "keyword_vector": [0.1, 0.5, 0.9],
    },
}

response = await client.post("/jobs/", json=payload)
```

### Read

``` python
# Get all jobs
response = await client.get("/jobs/")

# Get one job by job ID
response = await client.get(f"/jobs/{job_id}")
```

### Update

``` python
# Partial update salary range
patch = await client.patch(
    f"/jobs/{job_id}",
    json={
        "salary_range": {
            "min": 90000,
            "max": 130000,
        }
    },
)
```

### Delete

``` python
# Delete one job
delete = await client.delete(f"/jobs/{job_id}")

"""NOTE: Deleting a job with cause a cascading delete on: UserJobInteractions, JobMatches"""
```
------------------------------------------------------------------------

## job_matches

Stores ML-generated job recommendations with scoring and match context.

### Schema

``` json
{
  "_id": ObjectId,
  "user_id": ObjectId (FK, user_id references UserProfile._id),
  "job_id": ObjectId (FK, job_id references JobPosting._id),
  "relevancy_score": Number (0.0 - 1.0),
  "matched_at": ISODate,
  "match_reason": String,
  "is_active": Boolean,
  "match_details": {
    "skills_matched": Array<String>,
    "skills_missing": Array<String>,
    "overall_compatibility": Number
  },
  "user_snapshot": {
    "preferences_at_match": Object,
    "credentials_at_match": Object
  }
}
```

### Indexes

-   **Unique:** `_id`
-   **Unique:** `(user_id, job_id)`
-   Indexed: `user_id`
-   Indexed: `job_id`
-   Indexed: `relevancy_score`

### Important Constraint

Only **one job match per (user_id, job_id)** pair is allowed.

## CRUD Examples

### Create / Upsert

``` python
# Match one job to one user
payload = {
    "user_id": {user_id},
    "job_id": {job_id},
    "relevancy_score": 0.87,
    "match_reason": "Strong ML alignment",
    "match_details": {
        "skills_matched": ["Python", "ML"],
        "skills_missing": ["Docker"],
        "overall_compatibility": 0.9,
    },
    "user_snapshot": {
        "preferences_at_match": {"location": "Remote"},
        "credentials_at_match": {"years_experience": 3},
    },
}

response = await client.post("/job-matches/", json=payload)
```

### Read

``` python
# Get all job matches for one user
response = await client.get(f"/job-matches/user/{user_id}")
```

### Update

``` python
# Partial update relevancy score
patch = await client.patch(
    f"/job-matches/{match_id}",
    json={"relevancy_score": 0.95},
)

```

### Delete

``` python
# Delete one jobmatch
delete = await client.delete(f"/job-matches/{match_id}")
```

------------------------------------------------------------------------

## saved_searches

Stores roles that the user is interested in applying for.

### Schema

``` json
{
  "_id": ObjectId,
  "user_id": ObjectId (FK, user_id references UserProfile._id),
  "search_name": String,
  "search_query": Object,
  "total_matches": Number,
  "new_matches": Number,
  "last_viewed": ISODate,
  "last_match_check": ISODate,
  "created_at": ISODate
}
```

### Indexes

-   **Unique:** `_id`
-   Indexed: `user_id`

## CRUD Examples

### Create / Upsert

``` python
# Create one saved search
payload = {
    "user_id": user_id,
    "search_name": "Data Scientist Roles",
    "search_query": {
        "title": "data scientist",
        "location": "remote",
    },
}

res = await client.post("/saved-searches/", json=payload)
```

### Read

``` python
# Get all saved searches for one user
res = await client.get(f"/saved-searches/user/{user_id}")

# Get a saved search by ID
res = await client.get(f"/saved-searches/{search_id}")
```

### Update

``` python
# Partial update search_name parameter
patch = await client.patch(
    f"/saved-searches/{search_id}",
    json={"search_name": "Updated Name"},
)

# Update saved search parameters
put = await client.put(
    f"/saved-searches/{search_id}",
    json={
        "search_name": "New",
        "search_query": {"role": "frontend"},
    },
)
```

### Delete

``` python
# Delete one savedsearch
delete = await client.delete(f"/saved-searches/{search_id}",)
```

------------------------------------------------------------------------

## user_job_interactions

Tracks user engagement with job postings.

### Schema

``` json
{
  "_id": ObjectId,
  "user_id": ObjectId (FK, user_id references UserProfile._id),
  "job_id": ObjectId (FK, job_id references JobPosting._id),
  "interaction_type": "viewed | saved | applied | rejected | withdrawn",
  "timestamp": ISODate
}
```

### Indexes

-   **Unique:** `_id`
-   **Unique:** `(user_id, job_id, interaction_type)`
-   Indexed: `user_id`
-   Indexed: `job_id`

A user cannot perform the same interaction twice on the same job.

## CRUD Examples

### Create

``` python
# Create a user job interaction of type "viewed"
response = await client.post(
    "/interactions/",
    json={
        "user_id": user.json()["id"],
        "job_id": job.json()["id"],
        "interaction_type": "viewed",
    },
)
```

### Read

``` python
# Get interaction by user
response = await client.get(f"/interactions/user/{user_id}")

# Get interaction by job
response = await client.get(f"/interactions/job/{job_id}")
```

### Update

``` python
# Update interaction status from "viewed" to "saved"
patch = await client.patch(
    f"/interactions/{interaction_id}",
    json={"interaction_type": "saved"},
)
```

### Delete

``` python
# Delete one user job interaction
delete = await client.delete(f"/interactions/{interaction_id}")
```

------------------------------------------------------------------------

## user_stats

Stores aggregated engagement statistics per user.

### Schema

``` json
{
  "_id": ObjectId,
  "user_id": ObjectId (FK, user_id references UserProfile._id),
  "jobs_viewed": Number,
  "jobs_saved": Number,
  "top_missing_skill": String,
  "last_calculated": ISODate
}
```

### Index

-   **Unique:** `_id`
-   **Unique:** `user_id`

Only one stats document per user.

## CRUD Examples

### Create

``` python
# Auto-created upon UserProfile creation
```

### Read

``` python
# Get user stats for one user
res = await client.get(f"/users/{user_id}/stats")
```

### Update

``` python
# Update user stats for one user
patch = await client.patch(
    f"/users/{user_id}/stats",
    json={
        "jobs_viewed": 5,
        "jobs_saved": 2,
        "top_missing_skill": "Docker",
    },
)

# Update only jobs viewed
patch = await client.patch(
    f"/users/{user_id}/stats",
    json={"jobs_viewed": 10},
)
```

### Delete

``` python
# Auto-deleted upon UserProfile deletion
```

------------------------------------------------------------------------

# Connecting to MongoDB

``` python
# Load environment variables
load_dotenv()

# Set database name, use either PROD_DB or TEST_DB
db_name = os.getenv("TEST_DB")

# Connect to database
await mongo.connect(db_name)

# Load indexes for all collections
await ensure_indexes()

"""Add CRUD operations here"""

# Close connection to MongoDB
await mongo.close()
```

See example scripts in `backend/tests/db_crud_example.py` and `backend/tests/test_users_crud.py` to see how it's all put together.

How to run `backend/tests/db_crud_example.py`
``` python
# From root directory AIJobHunt/
python3 -m backend.tests.db_crud_example
```

How to run `backend/tests/test_users_crud.py`
``` python
# From root directory AIJobHunt/
python3 -m pytest backend/tests/test_users_crud.py
```