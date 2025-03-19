// Load shipment events history
async function loadAllShipmentEvents() {
    try {
        const response = await fetch(`http://127.0.0.1:8000/shipment_events`);
        if (!response.ok) throw new Error("Failed to fetch shipment events.");

        const events = await response.json();
        updateShipmentTable(events);
    } catch (error) {
        console.error("❌ Error loading shipment events:", error);
    }
}

// Update the shipment table
function updateShipmentTable(events) {
    const table = document.getElementById("shipmentTable");
    table.innerHTML = ""; // Clear table first

    events.forEach(event => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${event.tracking_number}</td>
            <td class="status">${event.status}</td>
            <td>${event.location}</td>
            <td>${event.timestamp}</td>
        `;
        table.appendChild(row);
    });
}

// WebSocket real-time updates
const socket = new WebSocket("ws://127.0.0.1:8000/ws");

socket.onopen = () => console.log("✅ WebSocket Connected");
socket.onerror = (error) => console.error("❌ WebSocket Error:", error);
socket.onclose = () => console.warn("⚠️ WebSocket Disconnected");

socket.onmessage = async function(event) {
    console.log("📡 Real-time update received:", event.data);

    // On WebSocket update, reload shipment events dynamically
    await loadAllShipmentEvents();
};

// Initial data load
loadAllShipmentEvents();