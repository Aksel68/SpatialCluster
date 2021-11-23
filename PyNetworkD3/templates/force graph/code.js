$main

const boundingBox = $bounding_box;
const forceLink = $force_link;
const forceSimulation = $force_simulation;
const forceCollision = $force_collision;
const MAX_RADIUS = $radio;

const tooltip = d3
    .select("body")
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

const simulation = d3
    .forceSimulation()
    .force("center", d3.forceCenter(widthSVG / 2, heightSVG / 2))
    .force("collision", d3.forceCollide(forceCollision))
    .force("charge", d3.forceManyBody().strength(forceSimulation))
    .force("link", d3.forceLink().id(node => node.id));

$code