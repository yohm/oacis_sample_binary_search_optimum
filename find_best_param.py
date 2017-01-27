import oacis

class Maximizer():

    def __init__( self, simulator, search_on, domain, resolution, other_params, target, create_runs, watcher ):
        self.sim = simulator
        self.search_on = search_on
        self.domain = domain
        self.resolution = resolution
        self.other_params = other_params
        self.target = target
        self.create_runs = create_runs
        self.watcher = watcher
        self.answer = None
        self.query = { "v.%s"%k:v for k,v in self.other_params.items() if k != self.search_on }

    def start_searching(self):
        param = self.other_params.copy()
        param[ self.search_on ] = self.domain[0]
        left_ps = self.sim.find_or_create_parameter_set( param )
        param[ self.search_on ] = self.domain[1]
        right_ps = self.sim.find_or_create_parameter_set( param )
        self.create_runs( left_ps )
        self.create_runs( right_ps )
        observed = self.sim.parameter_sets().where( self.query )
        self.watcher.watch_all_ps( observed, self._search_for_maximum )

    def _search_for_maximum(self, parameter_sets):
        best_ps = self._find_current_best_ps( parameter_sets )
        left_ps, right_ps = self._find_nearest_neighbors( best_ps )
        new_ps_list = []
        if (left_ps is not None) and abs(left_ps.v()[self.search_on]-best_ps.v()[self.search_on]) > self.resolution:
            new_ps1 = self._create_a_new_ps_in_between( left_ps, best_ps )
            new_ps_list.append(new_ps1)
        if (right_ps is not None) and abs(right_ps.v()[self.search_on]-best_ps.v()[self.search_on]) > self.resolution:
            new_ps2 = self._create_a_new_ps_in_between( right_ps, best_ps )
            new_ps_list.append(new_ps2)
        if len(new_ps_list) > 0:
            observed = self.sim.parameter_sets().where( self.query )
            self.watcher.watch_all_ps( observed, self._search_for_maximum )
        else:
            self.answer = best_ps

    def _find_current_best_ps(self, parameter_sets):
        sorted_by_output = sorted( parameter_sets, key=lambda ps: self.target(ps) )
        best_ps = sorted_by_output[-1]
        return best_ps

    def _find_nearest_neighbors( self, ps ):
        ps_list = list( ps.parameter_sets_with_different( self.search_on ) )
        idx = ps_list.index( ps )
        left_ps = ps_list[idx-1] if idx > 0 else None
        right_ps = ps_list[idx+1] if idx+1 < len(ps_list) else None
        return (left_ps, right_ps)

    def _create_a_new_ps_in_between( self, ps1, ps2 ):
        new_param = ps1.v()
        new_param[self.search_on] = (ps1.v()[self.search_on] + ps2.v()[self.search_on]) / 2.0
        new_ps = sim.find_or_create_parameter_set( new_param )
        self.create_runs( new_ps )
        return new_ps

if __name__ == "__main__":
    sim = oacis.Simulator.find_by_name("binary_search_optimum_test")
    def get_result(ps):
        return -ps.average_result("result")[0]
    def create_runs(ps):
        ps.find_or_create_runs_upto(1, submitted_to=oacis.Host.find_by_name("localhost") )
    other_params = {"p2": 0.3}
    w = oacis.OacisWatcher()
    m = Maximizer( simulator=sim, search_on="p1", domain=(0.0,1.0), resolution=0.1, other_params=other_params, target=get_result, create_runs=create_runs, watcher=w )
    m.start_searching()
    w.loop()

