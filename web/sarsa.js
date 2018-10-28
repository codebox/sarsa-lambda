"use strict";

const DELAY_MILLIS = 500;

function fetchJson(url, callback) {
    fetch(url).then(response => response.json()).then(obj => {
        setTimeout(() => callback(obj), DELAY_MILLIS);
    });
}

const grid = document.getElementById('grid');
function drawEnvironment(env) {
    const table = ['<table>'];

    env.forEach(row => {
        table.push('<tr>');
        row.forEach(cell => {
            table.push(`<td>${cell}</td>`);
        });
        table.push('</tr>');
    });
    table.push('</table>');

    grid.innerHTML = table.join('');
}

function init(){
    fetchJson('/init', env => {
        drawEnvironment(env);
        function move() {
            fetchJson(`/move/${JSON.stringify(env)}`, response => {
                env = response.env
                drawEnvironment(env);
                if (response.terminal) {
                    init();
                } else {
                    move();
                }
            });
        }
        move();
    });
}
init();
