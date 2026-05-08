const fs = require('fs');

// Read the file
const data = fs.readFileSync('test-input.txt', 'utf-8');
const lines = data.split('\n').filter(line => line.trim() !== '');

// Print the list of lines
console.log(lines);

let location = 50;
let zeroCounter = 0;
let pastZeroCounter = 0;

// Iterate through each line
for (const line of lines) {
    const previousLocation = location;
    console.log(`Location is currently: ${location}`);
    const cleanline = line.trim();
    console.log(`Processing line: ${cleanline}`);
    const direction = cleanline[0];
    const distance = parseInt(cleanline.substring(1));

    // Move one step at a time and check if we pass zero
    for (let i = 0; i < distance; i++) {
        if (direction === 'R') {
            location += 1;
        } else if (direction === 'L') {
            location -= 1;
        }

        location = location % 100;

        if (location === 0) {
            pastZeroCounter++;
            console.log(`Location went past zero! Total times: ${pastZeroCounter}`);
        }
    }
}

console.log(`Number of times location was zero: ${zeroCounter}`);
console.log(`Number of times location went past zero: ${pastZeroCounter}`);
console.log(`Total: ${zeroCounter + pastZeroCounter}`);
