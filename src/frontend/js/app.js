const API_URL = 'http://localhost:8080/api/rooms';

async function fetchRooms() {
    const loader = document.getElementById('loader');
    const grid = document.getElementById('grid-container');
    
    loader.classList.remove('hidden');
    grid.classList.add('hidden');

    try {
        const response = await fetch(API_URL);
        const rooms = await response.json();
        renderRooms(rooms);
    } catch (error) {
        console.error('Error fetching data:', error);
        grid.innerHTML = `<div class="col-span-full p-4 bg-red-50 text-red-600 rounded-lg text-center">Failed to connect to API</div>`;
    } finally {
        loader.classList.add('hidden');
        grid.classList.remove('hidden');
    }
}

function renderRooms(rooms) {
    const grid = document.getElementById('grid-container');
    grid.innerHTML = '';

    rooms.forEach(room => {
        const isAvailable = room.status === 'available';
        
        const card = document.createElement('div');
        card.className = `glass-panel rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden`;
        
        const stripColor = isAvailable ? 'bg-emerald-400' : 'bg-rose-400';
        
        card.innerHTML = `
            <div class="absolute left-0 top-0 bottom-0 w-1 ${stripColor}"></div>
            <div class="flex justify-between items-start mb-4">
                <div>
                    <span class="text-xs font-semibold uppercase tracking-wider text-slate-400 block mb-1">Room</span>
                    <h2 class="text-2xl font-semibold text-slate-800">${room.id}</h2>
                </div>
                <span class="status-badge px-2.5 py-1 rounded-full text-xs font-medium ${isAvailable ? 'bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/20' : 'bg-rose-50 text-rose-700 ring-1 ring-rose-600/20'}">
                    ${room.status.charAt(0).toUpperCase() + room.status.slice(1)}
                </span>
            </div>
            <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
                <span class="text-sm text-slate-500 capitalize flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                    ${room.type}
                </span>
            </div>
        `;
        grid.appendChild(card);
    });
}

document.addEventListener('DOMContentLoaded', fetchRooms);
