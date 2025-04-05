# AI Recommendation Engine

A modern recommendation engine that uses machine learning to provide personalized content suggestions based on user preferences and behavior.

## Features

- Content-based recommendation system
- User preference learning
- Real-time recommendations
- Modern web interface
- RESTful API

## Tech Stack

### Backend
- Python 3.9+
- FastAPI
- scikit-learn
- pandas
- numpy

### Frontend
- React
- TypeScript
- Material-UI
- Axios

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the backend server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## API Documentation

Once the backend server is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
.
├── app/
│   ├── main.py
│   ├── models/
│   ├── routers/
│   └── services/
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── requirements.txt
└── README.md
```

## Deployment Instructions

### AWS EC2 Deployment

1. **Create an EC2 Instance**:
   - Go to AWS Console → EC2 → Launch Instance
   - Choose Ubuntu Server 22.04 LTS
   - Select t2.micro (free tier) or larger based on your needs
   - Configure Security Group:
     - Allow inbound traffic on port 22 (SSH)
     - Allow inbound traffic on port 8000 (API)
     - Allow inbound traffic on port 80 (HTTP)
     - Allow inbound traffic on port 443 (HTTPS)

2. **Connect to Your EC2 Instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-public-ip
   ```

3. **Deploy the Application**:
   - Copy your application files to the EC2 instance:
     ```bash
     scp -i your-key.pem -r ./* ubuntu@your-ec2-public-ip:~/app/
     ```
   - SSH into your instance and run:
     ```bash
     chmod +x deploy.sh
     ./deploy.sh
     ```

4. **Environment Variables**:
   - Create a `.env` file on the EC2 instance with your production environment variables
   - Make sure to update the database connection string to point to your production database

5. **Access Your Application**:
   - API will be available at: `http://your-ec2-public-ip:8000`
   - Frontend will be available at: `http://your-ec2-public-ip`

### Important Notes:
- Make sure to update your `.env` file with production credentials
- Consider setting up a domain name and SSL certificate for production use
- Set up proper monitoring and logging
- Regularly backup your database
- Consider using AWS RDS for the database in production#   S H L - R C - E n g i n e  
 #   S H L - R C - E n g i n e  
 