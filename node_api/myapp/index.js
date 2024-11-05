const express = require('express');
const axios = require('axios');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
app.use(express.json());

const DECRYPTER_API_URL = process.env.DECRYPTER_URL;
const TRANSFORMER_API_URL = process.env.TRANSFORMER_URL;
const ENCRYPT_API_URL = process.env.ENCRYPT_URL;

app.get('/ping', (req, res) => {
    res.status(200).send("OK");
});

async function decryptData(inputData) {
    try {
        const decryptResponse = await axios.post(DECRYPTER_API_URL, {
            data: inputData,
        });
        return decryptResponse.data.data;
    } catch (error) {
        throw new Error(`Failed to decrypt data: ${error.response ? error.response.data : error.message}`);
    }
}

async function transformData(contextKey, decryptedData) {
    try {
        const transformResponse = await axios.post(TRANSFORMER_API_URL, {
            context: contextKey,
            data: decryptedData,
        });
        return transformResponse.data.data;
    } catch (error) {
        throw new Error(`Failed to transform data: ${error.response ? error.response.data : error.message}`);
    }
}

async function encryptData(transformedData) {
    try {
        const encryptResponse = await axios.post(ENCRYPT_API_URL, {
            data: transformedData,
        });
        return encryptResponse.data.encrypted_data;
    } catch (error) {
        throw new Error(`Failed to encrypt transformed data: ${error.response ? error.response.data : error.message}`);
    }
}

app.post('/process', async (req, res) => {
    const { data: inputData, context: contextKey } = req.body;

    if (!inputData || !contextKey) {
        return res.status(400).json({ error: "Missing data or context key" });
    }

    try {
        const decryptedData = await decryptData(inputData);
        const transformedData = await transformData(contextKey, decryptedData);
        const encryptedData = await encryptData(transformedData);

        return res.status(200).json({
            decrypted_data: decryptedData,
            transformed_data: transformedData,
            encrypted_data: encryptedData,
        });
    } catch (error) {
        return res.status(500).json({ error: `An error occurred: ${error.message}` });
    }
});

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
