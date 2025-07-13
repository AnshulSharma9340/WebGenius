// script.js
// Luminal Q ke frontend ki interactivity ko handle karta hai.

document.addEventListener('DOMContentLoaded', () => {
    const promptInput = document.getElementById('prompt-input');
    const generateButton = document.getElementById('generate-button');
    const statusDisplay = document.getElementById('status-display');
    const generatedUrlDisplay = document.getElementById('generated-url-display');
    const generatedUrlLink = generatedUrlDisplay.querySelector('a');

    generateButton.addEventListener('click', async () => {
        const prompt = promptInput.value.trim();

        if (!prompt) {
            statusDisplay.textContent = 'Please enter a valid prompt.';
            generatedUrlDisplay.classList.add('hidden');
            return;
        }

        statusDisplay.textContent = `"${prompt}" ke aadhar par application generate karne ke liye backend ko bhej raha hoon...`;
        generatedUrlDisplay.classList.add('hidden'); // URL display ko shuru mein hide karein
        console.log('Prompt from frontend:', prompt);

        try {
            const backendUrl = 'http://127.0.0.1:5000/generate-app'; // Backend API ka URL

            const response = await fetch(backendUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt }), // Prompt ko JSON format mein bhejte hain
            });

            const data = await response.json();

            if (response.ok) { // Agar status code 200-299 ke beech hai
                statusDisplay.textContent = `Backend response: ${data.message}`;
                console.log('Backend response:', data);

                if (data.generated_url) {
                    generatedUrlLink.href = data.generated_url;
                    generatedUrlLink.textContent = data.generated_url; // Full URL display karein
                    generatedUrlDisplay.classList.remove('hidden'); // URL display ko show karein
                }
            } else {
                // Agar response mein error hai
                statusDisplay.textContent = `Backend se error: ${data.error || 'Unknown error'}`;
                console.error('Backend error response:', data);
            }

        } catch (error) {
            console.error('Backend ko request bhejte samay error:', error);
            statusDisplay.textContent = 'Backend se communication mein error hui. Console dekhein.';
            generatedUrlDisplay.classList.add('hidden');
        }
    });
});
