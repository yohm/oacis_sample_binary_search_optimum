import oacis

def wait( parameter_sets ):
    w = oacis.OacisWatcher()
    w.watch_all_ps( parameter_sets, lambda pss: None)
    w.loop()
    
def find_nearest_neighbors( ps, input_key ):
    ps_list = list( ps.parameter_sets_with_different( input_key ) )
    idx = ps_list.index( ps )
    left_ps = ps_list[idx-1] if idx > 0 else None
    right_ps = ps_list[idx+1] if idx+1 < len(ps_list) else None
    return (left_ps, right_ps)

def find_optimum_ps( sim, input_key, output_key, base_param):
    query = { "v.%s"%k:v for k,v in base_param.items() if k != input_key }
    print(query)
    parameter_sets = sim.parameter_sets().where( query )
    print( len(parameter_sets) )
    wait( parameter_sets )
    sorted_by_output = sorted( parameter_sets, key=lambda ps: ps.average_result(output_key)[0] )
    best_ps = sorted_by_output[-1]
    return best_ps

def create_a_new_ps_in_between( ps1, ps2, input_key ):
    new_param = ps1.v()
    new_param[input_key] = (ps1.v()[input_key] + ps2.v()[input_key]) / 2.0
    new_ps = sim.find_or_create_parameter_set( new_param )
    new_runs = new_ps.find_or_create_runs_upto(1, submitted_to=oacis.Host.find_by_name("localhost") )
    return new_ps

def search_for_maximum( sim, input_key, output_key, base_param, resolution):
    best_ps = find_optimum_ps( sim, input_key, output_key, base_param )
    left_ps, right_ps = find_nearest_neighbors( best_ps, input_key )
    new_ps_list = []
    if (left_ps is not None) and abs(left_ps.v()[input_key]-best_ps.v()[input_key]) > resolution:
        new_ps1 = create_a_new_ps_in_between( left_ps, best_ps, input_key )
        new_ps_list.append(new_ps1)
    if (right_ps is not None) and abs(right_ps.v()[input_key]-best_ps.v()[input_key]) > resolution:
        new_ps2 = create_a_new_ps_in_between( right_ps, best_ps, input_key )
        new_ps_list.append(new_ps2)
    if len(new_ps_list) > 0:
        return search_for_optimum( sim, input_key, output_key, base_param, resolution)
    else:
        return best_ps

class Maximizer():

    def __init__( simulator, search_on, domain, resolution, other_params, target, create_runs, watcher ):
        self.sim = simulator
        self.search_on = search_on
        self.domain = domain
        self.resolution = resolution
        self.other_params = other_params
        self.target = target
        self.create_runs = create_runs
        self.watcher = watcher
        self.ansewr = None
        self.query = { "v.%s"%k:v for k,v in self.other_params.items() if k != self.search_on }

    def start_searching():
        param = self.other_params.copy()
        param[ self.search_on ] = self.domain[0]
        left_ps = simulator.find_or_create_parameter_set( param )
        param[ self.search_on ] = self.domain[1]
        right_ps = simulator.find_or_create_parameter_set( param )
        self.create_runs( left_ps )
        self.create_runs( right_ps )
        observed = self.sim.parameter_sets().where( query )
        self.watcher.watch_all_ps( observed, self._search_for_maximum )

    def _search_for_maximum():
        pass


if __name__ == "__main__":
    sim = oacis.Simulator.find_by_name("binary_search_optimum_test")
    def get_result(ps):
        return ps.average_result("result")[0]
    def create_runs(ps):
        ps.find_or_create_runs_upto(1, submitted_to=oacis.Host.find_by_name("localhost") )
    other_params = {"p2": 0.3}
    w = oacis.OacisWatcher()
    get_maximum_ps_future( simulator=sim, search_on="p1", domain=(0.0,1.0), resolution=0.05, other_params=other_params, target=get_result, create_runs=create_runs, watcher=w )
    w.loop()

