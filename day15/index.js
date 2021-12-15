const fs = require("fs");

const readFile = (filename) =>
  fs
    .readFileSync(filename)
    .toString()
    .trim()
    .split("\n")
    .map((line) => line.split("").map((n) => parseInt(n, 10)));

function expandCave(cave) {
  const rows = cave.length;
  const cols = cave[0].length;
  expanded = [];

  for (let i = 0; i < rows * 5; i++) {
    const row = [];
    for (let j = 0; j < cols * 5; j++) {
      const orig = cave[i % rows][j % cols];
      to_add = Math.floor(i / rows) + Math.floor(j / cols);
      row.push(orig + to_add > 9 ? (orig + to_add) % 9 : orig + to_add);
    }
    expanded.push(row);
  }

  return expanded;
}

function safestPath(cave) {
  const rows = cave.length;
  const cols = cave[0].length;
  let cost = Array();

  const dx = [-1, 0, 1, 0];
  const dy = [0, 1, 0, -1];

  for (let i = 0; i < rows; i++) {
    let row = [];
    for (let j = 0; j < cols; j++) {
      row.push(Infinity);
    }
    cost.push(row);
  }
  cost[0][0] = 0;

  queue = [{ x: 0, y: 0 }];

  while (queue.length) {
    const { x, y } = queue.shift();

    for (let i = 0; i < 4; i++) {
      const nx = x + dx[i];
      const ny = y + dy[i];

      if (nx < 0 || nx >= cols || ny < 0 || ny >= rows) {
        continue;
      }

      entryCost = cost[x][y] + cave[nx][ny];

      if (entryCost < cost[nx][ny]) {
        cost[nx][ny] = entryCost;
        queue.push({ x: nx, y: ny });
      }
    }
  }

  return cost[rows - 1][cols - 1];
}

function part1(cave) {
  return safestPath(cave);
}
function part2(cave) {
  return safestPath(expandCave(cave));
}

require.main === module &&
  console.log(
    (process.env.part === "part2" ? part2 : part1)(readFile("input.txt"))
  );
