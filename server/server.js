const express = require('express');
const mongoose = require('mongoose');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const genAI = new GoogleGenerativeAI({
    apiKey: process.env.GEMINI_API_KEY,
});

// Route to generate a financial literacy question using Gemini API
app.get('/api/questions', async (req, res) => {
    try {
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const prompt = "Generate a financial literacy question for beginners";

        // Call the correct method to generate content
        const result = await model.generateContent({
            prompt: prompt,
            max_tokens: 100,
        });

        // Send back the generated question as a response
        res.json({ question: result.candidates[0].output });
    } catch (error) {
        console.error("Error generating question:", error.message);
        res.status(500).send("Error generating question");
    }
});

const PORT = process.env.PORT || 5000;

// Basic route for testing
app.get('/', (req, res) => {
    res.send('Backend is running!');
});

// Connect to MongoDB Atlas using Mongoose
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log("MongoDB connected"))
    .catch(err => console.error("MongoDB connection error:", err));

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});