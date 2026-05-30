import { readFileSync } from "fs";
import { createInterface } from "readline";

// Load words
const words = readFileSync("words.txt", "utf-8")
    .split("\n")
    .map(w => w.trim())
    .filter(w => w.length === 5);

let candidates = [...words];

// ✅ CORRECT Wordle feedback simulation
function getFeedback(guess, answer) {
    const result = Array(5).fill("b");
    const answerArr = answer.split("");

    // greens
    for (let i = 0; i < 5; i++) {
        if (guess[i] === answer[i]) {
            result[i] = "g";
            answerArr[i] = null;
        }
    }

    // yellows
    for (let i = 0; i < 5; i++) {
        if (result[i] === "b") {
            const idx = answerArr.indexOf(guess[i]);
            if (idx !== -1) {
                result[i] = "y";
                answerArr[idx] = null;
            }
        }
    }

    return result.join("");
}

// ✅ FIXED filter (uses real Wordle logic)
function filterWords(words, guess, result) {
    return words.filter(word => getFeedback(guess, word) === result);
}

// Frequency scoring
function getFrequency(words) {
    const freq = {};
    for (const word of words) {
        for (const char of new Set(word)) {
            freq[char] = (freq[char] || 0) + 1;
        }
    }
    return freq;
}

function scoreWord(word, freq) {
    let score = 0;
    for (const char of new Set(word)) {
        score += freq[char] || 0;
    }
    return score;
}

function suggest(words) {
    const freq = getFrequency(words);
    return words
        .map(w => ({ word: w, score: scoreWord(w, freq) }))
        .sort((a, b) => b.score - a.score)
        .slice(0, 10);
}

// CLI
const rl = createInterface({
    input: process.stdin,
    output: process.stdout
});

function ask() {
    console.log("\nTop suggestions:");
    suggest(candidates).forEach(s => {
        console.log(`${s.word} (${s.score})`);
    });

    rl.question("\nEnter guess: ", guess => {
        if (guess.length !== 5) {
            console.log("❌ Guess must be 5 letters");
            return ask();
        }

        rl.question("Enter result (g/y/b): ", result => {
            if (!/^[gyb]{5}$/.test(result)) {
                console.log("❌ Invalid result format");
                return ask();
            }

            if (result === "ggggg") {
                console.log("🎉 Solved!");
                rl.close();
                return;
            }

            candidates = filterWords(candidates, guess, result);

            console.log(`Remaining words: ${candidates.length}`);

            if (candidates.length === 0) {
                console.log("❌ No possible words (check input)");
                rl.close();
            } else if (candidates.length === 1) {
                console.log("✅ Answer:", candidates[0]);
                rl.close();
            } else {
                ask();
            }
        });
    });
}

console.log("Wordle Solver Started!");
ask();