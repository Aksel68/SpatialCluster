$main
const wordSize = Math.log(360 / dataset.nodes.length) * widthSVG / 2.5 * 0.04

container
    .selectAll("text")
    .data(dataset.nodes)
    .enter()
    .append("text")
    .attr("class", "node")
    .style("font-size", `${wordSize}px`)
    .text(d => d.id)

let maxSize = 0
document.querySelectorAll(".node").forEach(d => {
    maxSize = Math.max(d.getBBox().width, maxSize);
});

const radius = widthSVG / 2 - maxSize
const angle = d3.scaleLinear()
    .range([0, 360])
    .domain([0, dataset.nodes.length])
const x = (angle) => radius * Math.sin(Math.PI * 2 * angle / 360);
const y = (angle) => radius * Math.cos(Math.PI * 2 * angle / 360);
const curve = d3.line().curve(d3.curveBundle.beta(0.5));

let idToNode = {};
dataset.nodes.forEach(function(n, i) {
    idToNode[n.id] = n;
    actualAngle = angle(i);
    n.angle = actualAngle
    let actualX = x(actualAngle)
    let actualY = y(actualAngle)
    n.x = actualX + widthSVG / 2
    n.y = actualY + heightSVG / 2
});

dataset.links.forEach((e) => {
    e.source = idToNode[e.source];
    e.target = idToNode[e.target];
});

container
    .selectAll("text")
    .attr("transform", (d) => {
        let angle = d.angle < 180 ? -d.angle + 90 : -d.angle - 90
        return `translate(${d.x}, ${d.y}) rotate(${angle})`
    })
    .attr("text-anchor", d => d.angle < 180 ? "start" : "end")
    .attr("dominant-baseline", "central")

container
    .data(dataset.links)
    .enter()
    .each(d => {
        let middleX = (d.source.x + d.target.x) / 2
        let middleY = (d.source.y + d.target.y) / 2
        let points = [
            [d.source.x, d.source.y],
            [(middleX + widthSVG / 2) / 2, (middleY + widthSVG / 2) / 2], // intermediate point
            [d.target.x, d.target.y],
        ]
        container.append('path').attr('d', curve(points)).attr('fill', 'none');
    })