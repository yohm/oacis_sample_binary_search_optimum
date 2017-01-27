sim_name = "binary_search_optimum_test"
if sim = Simulator.where(name: sim_name).first
  $stderr.puts "already Simulator '#{sim_name}' exists. Deleting this."
  sim.discard
end
sim = Simulator.create!(
  name: sim_name,
  parameter_definitions: [
    {key: "p1", type: "Float", default: 0.0},
    {key: "p2", type: "Float", default: 0.5}
  ],
  command: 'ruby -r json -e \'prm=JSON.load(File.open("_input.json")); puts({"result"=>(prm["p1"]-prm["p2"]).abs}.to_json)\' > _output.json',
  executable_on: [Host.find_by_name("localhost")]
)
$stderr.puts "A new simulator #{sim.id} is created."

