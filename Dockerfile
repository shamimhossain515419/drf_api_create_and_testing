# Step 1: Use official Python image
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy Pipenv files to the container
COPY Pipfile Pipfile.lock ./

# Step 4: Install pipenv and dependencies
RUN pip install pipenv && pipenv install --dev

# Step 5: Copy all project files to the container
COPY . .

# Step 6: Run the Django development server
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
