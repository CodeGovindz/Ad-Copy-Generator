let savedData = null;

document.getElementById('adForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    if (!data.url && !data.product) {
        alert('Please provide either a website URL or product/service details.');
        return;
    }
    
    savedData = data;
    document.getElementById('loading').style.display = 'block';
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        
        console.log('Response:', response);
        
        if (response.ok) {
            const result = await response.json();
            console.log('Result:', result);
            
            if (result.ad_copy) {
                document.getElementById('adCopy').value = result.ad_copy;
                document.getElementById('result').style.display = 'block';
                autoResizeTextarea();
            } else {
                throw new Error('No ad copy in response');
            }
        } else {
            throw new Error('Server responded with an error');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = `<h2>Error:</h2><p>${error.message}</p>`;
        document.getElementById('result').style.display = 'block';
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
});

function editAdCopy() {
    const adCopy = document.getElementById('adCopy');
    const editBtn = document.getElementById('edit-btn');
    if (adCopy.readOnly) {
        adCopy.readOnly = false;
        adCopy.focus();
        editBtn.textContent = 'Save';
    } else {
        adCopy.readOnly = true;
        editBtn.textContent = 'Edit';
    }
}

function copyAdCopy() {
    const adCopy = document.getElementById('adCopy').value;
    navigator.clipboard.writeText(adCopy).then(() => {
        alert('Ad copy copied to clipboard!');
    });
}

async function regenerateAdCopy() {
    if (!savedData) return;
    document.getElementById('loading').style.display = 'block';
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(savedData),
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const result = await response.json();
        
        if (result.ad_copy) {
            document.getElementById('adCopy').value = result.ad_copy;
            autoResizeTextarea();
        } else {
            throw new Error('Failed to regenerate ad copy');
        }
    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function autoResizeTextarea() {
    const adCopy = document.getElementById('adCopy');
    adCopy.style.height = 'auto';
    adCopy.style.height = `${adCopy.scrollHeight}px`;
}
document.getElementById('edit-btn').addEventListener('click', editAdCopy);
document.getElementById('copy-btn').addEventListener('click', copyAdCopy);
document.getElementById('regenerate-btn').addEventListener('click', regenerateAdCopy);
