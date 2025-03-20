async function fetchShipmentEvents() {
    try {
        console.log("📡 Fetching shipment events..."); // Debugging Log

        const response = await fetch("http://127.0.0.1:8000/shipments/events");
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const events = await response.json();
        console.log("✅ Data received:", events); // Debugging Log

        const table = document.getElementById("shipmentEventsTable");
        table.innerHTML = "";  // Clear existing table data

        if (events.length === 0) {
            console.warn("⚠️ No shipment events found.");
            return;
        }

        events.forEach(event => {
            let newRow = document.createElement("tr");
            newRow.innerHTML = `
                <td>${event.tracking_number}</td>
                <td class="status ${event.status.toLowerCase()}">${event.status}</td>
                <td>${event.location}</td>
                <td>${new Date(event.timestamp).toLocaleString()}</td>
            `;
            table.appendChild(newRow);
        });

    } catch (error) {
        console.error("❌ Error fetching shipment events:", error);
    }
}

// Fetch events when the page loads
fetchShipmentEvents();