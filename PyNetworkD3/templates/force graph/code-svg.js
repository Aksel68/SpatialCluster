const ticked = () => {
    if (boundingBox) {
        container
            .selectAll(".node")
            .attr("cx", function(d) { return (d.x = Math.max(MAX_RADIUS, Math.min(widthSVG - MAX_RADIUS, d.x))); })
            .attr("cy", function(d) { return (d.y = Math.max(MAX_RADIUS, Math.min(heightSVG - MAX_RADIUS, d.y))); })
    }
    container
        .selectAll(".node")
        .attr("transform", node => `translate(${node.x}, ${node.y})`);

    container
        .selectAll("line")
        .attr("x1", link => link.source.x)
        .attr("y1", link => link.source.y)
        .attr("x2", link => link.target.x)
        .attr("y2", link => link.target.y);
};

const dragstarted = (event, node) => {
    if (!event.active) {
        simulation.alphaTarget(0.3).restart();
    }
    node.fx = node.x;
    node.fy = node.y;
};

const dragged = (event, node) => {
    node.fx = event.x;
    node.fy = event.y;
};

const dragended = (event, node) => {
    if (!event.active) {
        simulation.alphaTarget(0.0);
    }
    node.fx = null;
    node.fy = null;
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


const lineWidth = d3.scaleLinear()
    .range([0.5, 4])
    .domain(d3.extent(dataset.links.map(d => d.value)))

container
    .selectAll("line")
    .data(dataset.links)
    .enter()
    .append("line")
    .attr("x1", link => link.source.x)
    .attr("y1", link => link.source.y)
    .attr("x2", link => link.target.x)
    .attr("y2", link => link.target.y)
    .attr("stroke-width", link => link.value ? `${lineWidth(link.value)}px` : `1px`);

const nodes = container
    .selectAll(".node")
    .data(dataset.nodes)
    .enter()
    .append("g")
    .attr("class", "node")
    .call(
        d3
        .drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended)
    );


nodes
    .append("circle")
    .attr("r", MAX_RADIUS)
    .on("mouseover", mouseover)
    .on("mouseout", mouseout)