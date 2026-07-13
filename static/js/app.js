// Initialisation au chargement
document.addEventListener('DOMContentLoaded', () => {
    console.log('Souffle V2.0 - Application chargée ✅');
});

// Formatage des nombres en XOF
function formatXOF(value) {
    return new Intl.NumberFormat('fr-FR').format(Math.round(value));
}

// Fonction générique pour les appels API
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(endpoint, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}