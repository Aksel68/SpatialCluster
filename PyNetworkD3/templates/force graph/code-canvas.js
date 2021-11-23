context = container.getContext('2d');
const lineWidth = d3.scaleLinear()
    .range([0.5, 4])
    .domain(d3.extent(dataset.links.map(d => d.value)))

const ticked = () => {
    context.save();
    context.clearRect(0, 0, widthSVG, heightSVG);
    // Draw the nodes
    if (boundingBox) {
        dataset.nodes.forEach(d => {
            d.x = Math.max(MAX_RADIUS, Math.min(widthSVG - MAX_RADIUS, d.x))
            d.y = Math.max(MAX_RADIUS, Math.min(heightSVG - MAX_RADIUS, d.y))
        })
    }
    context.strokeStyle = '#9ECAE1'
    dataset.links.forEach(d => {
        context.beginPath();
        context.lineWidth = d.value ? lineWidth(d.value) : 4
        context.moveTo(d.source.x, d.source.y);
        context.lineTo(d.target.x, d.target.y);
        context.stroke();
    });

    dataset.nodes.forEach(d => {
        context.beginPath();
        context.arc(d.x, d.y, MAX_RADIUS, 0, 2 * Math.PI, true);
        context.fillStyle = "#FD8D3C"
        context.fill();
    });

    context.restore();

};
const dragstarted = (event) => {
    if (!event.active) {
        simulation.alphaTarget(0.3).restart();
    }
    event.subject.fx = event.x
    event.subject.fy = event.y
};

const dragged = (event) => {
    event.subject.fx = event.x
    event.subject.fy = event.y
};

const dragended = (event) => {
    if (!event.active) {
        simulation.alphaTarget(0.0);
    }
    event.subject.fx = null;
    event.subject.fy = null;
};

const mouseover = (event, node) => {
    if (tooltipAttributes) {
        let content = '<table style="margin-top: 2.5px;">'
        tooltipAttributes.forEach(d => {
            content += `<tr><td>${d}: </td><td style="text-align: right">${node[d]}</td></tr>`
        })
        content += '</table>'

        tooltip
            .transition()
            .duration(200)
            .style("opacity", 0.9);

        tooltip
            .html(content)
            .style("left", event.pageX + "px")
            .style("top", event.pageY - 28 + "px");
    }
};

const mouseout = _ => {
    if (tooltipAttributes) {
        tooltip
            .transition()
            .duration(200)
            .style("opacity", 0);
    }
};

simulation
    .nodes(dataset.nodes)
    .on("tick", ticked)
    .force("link")
    .links(dataset.links)
    .distance(d => forceLink);


const dragsubject = (event) => {
    for (let i = dataset.nodes.length - 1; i >= 0; --i) {
        node = dataset.nodes[i];
        dx = event.x - node.x;
        dy = event.y - node.y;
        if (dx * dx + dy * dy < MAX_RADIUS * MAX_RADIUS) {
            return node;
        }
    }
}
d3.select(container).call(
    d3.drag().subject(dragsubject)
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended)
)