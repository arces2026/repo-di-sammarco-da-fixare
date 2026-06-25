export default async function getProducts(){
    
    try {
        const response = await fetch('http://localhost:8000/api/v1/scarpe')
        
        // Controllo manuale dello stato HTTP
        if (!response.ok) {
            throw new Error(`Errore HTTP: ${response.status}`)
        }
        const data = await response.json()
        console.log({data: data.results})
        return data.results // Ritorna i dati puliti
    } catch (error) {
        console.error("Errore nel recupero dei prodotti:", error)
        throw error // Rilancia l'errore per gestirlo nel componente (es. mostrare un alert)
    }
}