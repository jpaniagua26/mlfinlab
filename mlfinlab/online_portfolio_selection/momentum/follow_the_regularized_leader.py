# pylint: disable=missing-module-docstring
import cvxpy as cp
from mlfinlab.online_portfolio_selection import FollowTheLeader


class FollowTheRegularizedLeader(FollowTheLeader):
    """
    This class implements the Follow the Regularized Leader strategy. It is reproduced with modification from the following paper:
    Li, B., Hoi, S. C.H., 2012. OnLine Portfolio Selection: A Survey. ACM Comput. Surv. V, N, Article A (December YEAR),
    33 pages. DOI:http://dx.doi.org/10.1145/2512962.

    Follow the Regularized Leader strategy directly tracks the Best Constant Rebalanced Portfolio until the previous
    period with an additional regularization term
    """
    def __init__(self, beta=0.1):
        """
        Beta is the regularization term

        :param beta: (float) a constant multiple to the regularization term
        """
        self.beta = beta
        super(FollowTheRegularizedLeader, self).__init__()

    # optimize the weight that maximizes the returns
    def optimize(self,
                 _optimize_array,
                 _solver=cp.SCS):
        """
        Calculates weights that maximize returns over a given _optimize_array

        :param _optimize_array: (np.array) relative returns of the assets for a given time period
        :param _solver: (cp.SOLVER) set the solver to be a particular cvxpy solver
        :return weights.value: (np.array) weights that maximize the returns for the given optimize_array
        """
        weights = cp.Variable(self.number_of_assets)
        # added additiona l2 regularization term for the weights for calculation
        portfolio_return = cp.sum(cp.log(_optimize_array * weights)) - self.beta * cp.norm(weights) / 2

        # optimization objective and constraints
        allocation_objective = cp.Maximize(portfolio_return)
        allocation_constraints = [cp.sum(weights) == 1, cp.min(weights) >= 0]
        # Define and solve the problem
        problem = cp.Problem(objective=allocation_objective, constraints=allocation_constraints)
        problem.solve(warm_start=True, solver=_solver)
        return weights.value
