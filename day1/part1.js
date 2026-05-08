const fs = require('fs');

// Read the file
const data = fs.readFileSync('input.txt', 'utf-8');
const lines = data.split('\n').filter(line => line.trim() !== '');

// Print the list of lines
console.log(lines);

let location = 50;
let zeroCounter = 0;

// Iterate through each line
for (const line of lines) {
    console.log(`Location is currently: ${location}`);
    const cleanline = line.trim();
    console.log(`Processing line: ${cleanline}`);
    const direction = cleanline[0];
    const distance = parseInt(cleanline.substring(1));

    if (direction === 'R') {
        location += distance;
    } else if (direction === 'L') {
        location -= distance;
    }

    location = location % 100;

    if (location === 0) {
        zeroCounter++;
    }
}

console.log(`Number of times location was zero: ${zeroCounter}`);
