import math
import sympy as sym
from numpy import linalg as la
import numpy as np
from copy import deepcopy
from scipy import integrate
x, y, z, i, j, k, t = sym.symbols('x y z i j k t')


def magnitude(vector):
    mag_squared = 0
    for units in vector:
        square = units*units
        mag_squared += square
    return math.sqrt(mag_squared)


def dot_product(vector1, vector2):
    if len(vector1) == len(vector2):
        value = 0
        i = -1
        while i < len(vector1) - 1:
            value += vector1[i]*vector2[i]
            i += 1
        return value
    else:
        print("Vector dimensions must be consistent.")


def cross_product(vector1, vector2):
    if len(vector1) == 3 and len(vector2) == 3:
        i = (vector1[1]*vector2[2]) - (vector1[2]*vector2[1])
        j = (vector1[2]*vector2[0]) - (vector1[0]*vector2[2])
        k = (vector1[0]*vector2[1]) - (vector1[1]*vector2[0])
        return [i, j, k]
    else:
        print("Vector must have 3 dimensions.")


def triple_scalar_product(vector1, vector2, vector3):  # finds volume of parallelepiped
    i = vector3[0] * ((vector1[1] * vector2[2]) - (vector1[2] * vector2[1]))
    j = vector3[1] * ((vector1[2] * vector2[0]) - (vector1[0] * vector2[2]))
    k = vector3[2] * ((vector1[0] * vector2[1]) - (vector1[1] * vector2[0]))
    volume = abs(i + j + k)
    return volume


def find_angle(vector1, vector2):  # angle between vectors
    dot_prod = dot_product(vector1, vector2)
    cos_theta = dot_prod / (magnitude(vector1) * magnitude(vector2))
    degrees = 180 * math.acos(cos_theta) / math.pi
    return round(degrees, 3)


def eigenvector(matrix):  # matrix in the form [[a, b],
    #                                           [c, d]]
    array = np.array(matrix)
    eigenvalues, eigenvectors = la.eig(array)
    set1 = (eigenvalues[0], [eigenvectors[0][0], eigenvectors[1][0]])
    print("Eigenvalue is: " + str(set1[0]) + ". Corresponding unit eigenvector is: " + str(set1[1]))
    set2 = (eigenvalues[1], [eigenvectors[0][1], eigenvectors[1][1]])
    print("Eigenvalue is: " + str(set2[0]) + ". Corresponding unit eigenvector is: " + str(set2[1]))
    return set1, set2, eigenvalues, eigenvectors


def two_dimensional_gradient(function):  # returns grad(f) of a scalar field
    diff_x = sym.diff(function, x)
    diff_y = sym.diff(function, y)
    gradient = [diff_x, diff_y]
    return gradient


def three_dimensional_gradient(function):
    diff_x = sym.diff(function, x)
    diff_y = sym.diff(function, y)
    diff_z = sym.diff(function, z)
    gradient = [diff_x, diff_y, diff_z]
    return gradient


def directional_derivative(function, point, direction):
    if len(point) == 2:
        grad = two_dimensional_gradient(function)
        mag = magnitude(direction)
        dot = dot_product(direction, grad) / mag
        sub_x = dot.subs(x, point[0])
        result = sub_x.subs(y, point[1])

    elif len(point) == 3:
        grad = three_dimensional_gradient(function)
        mag = magnitude(direction)
        dot = dot_product(direction, grad) / mag
        sub_x = dot.subs(x, point[0])
        sub_y = sub_x.subs(y, point[1])
        derivative = sub_y.subs(z, point[2])
    return derivative


def gradient_of_scalar(scalar, point): # finds gradient/ direction of scalar field
    grad = []
    if len(point) == 2:
        gradient = two_dimensional_gradient(scalar)
        for variable in gradient:
            grad_x = variable.subs(x, point[0])
            grad_y = grad_x.subs(y, point[1])
            grad.append(grad_y)

    elif len(point) == 3:
        gradient = three_dimensional_gradient(scalar)
        for variable in gradient:
            grad_x = variable.subs(x, point[0])
            grad_y = grad_x.subs(y, point[1])
            grad_z = grad_y.subs(z, point[2])
            grad.append(grad_z)
    return grad


def tangent_plane_of_surface(surface, point):  # returns answer in format [[x, y, z], scalar]
    grad = gradient_of_scalar(surface, point)
    scalar = dot_product(grad, point)
    tangent = [grad, scalar]
    return tangent


def stationary_values_2variables(function):
    f_x = two_dimensional_gradient(function)[0]
    f_y = two_dimensional_gradient(function)[1]

    answer = sym.solve([f_x, f_y], (x, y))

    f_xx = two_dimensional_gradient(f_x)[0]
    f_xy = two_dimensional_gradient(f_x)[1]
    f_yx = two_dimensional_gradient(f_y)[0]
    f_yy = two_dimensional_gradient(f_y)[1]
    hessian = [[f_xx, f_xy], [f_yx, f_yy]]

    variables = []
    if type(answer) is dict:
        soltuions = []
        for key, value in answer.items():
            soltuions.append(value)
        answer = soltuions
        variables.append(answer)
    else:
        variables = answer

    for solution in variables:
        solved_hessian = []
        for row in hessian:
            new_row =[]
            for column in row:
                hessian_x = column.subs(x, solution[0])
                hessian_xy = hessian_x.subs(y, solution[1])
                new_row.append(hessian_xy)
            solved_hessian.append(new_row)
        array = np.array(solved_hessian, dtype=np.float32)
        eigenvalues, eigenvectors = la.eig(array)
        if eigenvalues[0] * eigenvalues[1] > 0 and eigenvalues[0] + eigenvalues[1] > 0:
            print('Stationary point {}, has the eigenvalues {}, therefore is a minimum'.format(solution, eigenvalues))

        elif eigenvalues[0] * eigenvalues[1] > 0 and eigenvalues[0] + eigenvalues[1] < 0:
            print('Stationary point {}, has the eigenvalues {}, therefore is a maximum'.format(solution, eigenvalues))

        elif eigenvalues[0] * eigenvalues[1] < 0:
            print('Stationary point {}, has the eigenvalues {}, therefore is a saddle point'.format(solution, eigenvalues))


def stationary_values_3variables(function):
    f_x = three_dimensional_gradient(function)[0]
    f_y = three_dimensional_gradient(function)[1]
    f_z = three_dimensional_gradient(function)[2]

    answer = sym.solve([f_x, f_y, f_z], (x, y, z))

    f_xx = three_dimensional_gradient(f_x)[0]
    f_xy = three_dimensional_gradient(f_x)[1]
    f_xz = three_dimensional_gradient(f_x)[2]

    f_yx = three_dimensional_gradient(f_y)[0]
    f_yy = three_dimensional_gradient(f_y)[1]
    f_yz = three_dimensional_gradient(f_y)[2]

    f_zx = three_dimensional_gradient(f_z)[0]
    f_zy = three_dimensional_gradient(f_z)[1]
    f_zz = three_dimensional_gradient(f_z)[2]
    hessian = [[f_xx, f_xy, f_xz], [f_yx, f_yy, f_yz], [f_zx, f_zy, f_zz]]

    variables = []
    if type(answer) is dict:
        soltuions = []
        for key, value in answer.items():
            soltuions.append(value)
        answer = soltuions
        variables.append(answer)
    else:
        variables = answer

    for solution in variables:
        solved_hessian = []
        for row in hessian:
            new_row =[]
            for column in row:
                hessian_x = column.subs(x, solution[0])
                hessian_xy = hessian_x.subs(y, solution[1])
                hessian_xyz = hessian_xy.subs(z, solution[2])
                new_row.append(hessian_xyz)
            solved_hessian.append(new_row)
        try:
            array = np.array(solved_hessian, dtype=np.float32)
        except TypeError:
            continue
        eigenvalues, eigenvectors = la.eig(array)

        if np.sign(eigenvalues[0]) == 1 and np.sign(eigenvalues[1]) == 1 and np.sign(eigenvalues[2]) == 1:
            print('Stationary point {}, has the eigenvalues {}, therefore is a minimum'.format(solution, eigenvalues))

        elif np.sign(eigenvalues[0]) == -1 and np.sign(eigenvalues[1]) == -1 and np.sign(eigenvalues[2]) == -1:
            print('Stationary point {}, has the eigenvalues {}, therefore is a maximum'.format(solution, eigenvalues))

        else:
            print('Stationary point {}, has the eigenvalues {}, therefore is a saddle point'.format(solution,
                                                                                                    eigenvalues))


def divergent(vector_field):  # all maths functions passed through must use sym. instead of math.
    var_x = sym.diff(vector_field[0], x)
    var_y = sym.diff(vector_field[1], y)
    var_z = sym.diff(vector_field[2], z)
    return var_x + var_y + var_z


def curl(vector_field):  # all maths functions passed through must use sym. instead of math.
    I = sym.diff(vector_field[2], y) - sym.diff(vector_field[1], z)
    J = sym.diff(vector_field[0], z) - sym.diff(vector_field[2], x)
    K = sym.diff(vector_field[1], x) - sym.diff(vector_field[0], y)
    return[I, J, K]


def arc_length(function, lower_bound, upper_bound):
    mag_squared = 0
    for term in function:
        mag_squared += (sym.diff(term, t))**2
    mag_rdash = sym.sqrt(mag_squared)
    s = sym.Integral(mag_rdash, (t, lower_bound, upper_bound)).evalf()
    return s


def scalar_path_integral(integral, parametrised_function, bounds):
    mag_squared = 0
    for term in parametrised_function:
        mag_squared += (sym.diff(term, t))**2
    mag_diff_r = sym.sqrt(mag_squared)
    integralx = integral.subs(x, parametrised_function[0])
    integralxy = integralx.subs(y, parametrised_function[1])
    integralxyz = integralxy.subs(z, parametrised_function[2])
    s = sym.Integral(integralxyz * mag_diff_r, (t, bounds[0], bounds[1])).evalf()
    return s


def work_integral(integral, parametrised_function, bounds):
    diff_r = []
    for term in parametrised_function:
        diff_r.append(sym.diff(term, t))
    work = dot_product(diff_r, integral)
    integralx = work.subs(x, parametrised_function[0])
    integralxy = integralx.subs(y, parametrised_function[1])
    integralxyz = integralxy.subs(z, parametrised_function[2])
    s = sym.Integral(integralxyz, (t, bounds[0], bounds[1])).evalf()
    return s


def double_integral(function, y_bounds, x_bounds):
    return integrate.dblquad(function, x_bounds[0], x_bounds[1],
                             y_bounds[0], y_bounds[1])[0]
    # example function
    # Function = lambda x, y: x + y
    # x_bound = [1, 2]
    # y_bound = [lambda x: 0, lambda x: 4 -x**2]


def double_integral_parametrised(function, r_bounds, theta_bounds):
    return integrate.dblquad(function, r_bounds[0], r_bounds[1],
                             theta_bounds[0], theta_bounds[1])[0]
    # example function
    # Function = lambda t, r: np.sin(t) * r**2
    # r_bound = [0, 1]
    # t_bound = [0, math.pi]


def triple_integral(function, x_bounds, y_bounds, z_bounds):
    return integrate.tplquad(function, x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1],
                             z_bounds[0], z_bounds[1])
    # example function
    # function = lambda x, y, z: x + y + z
    # z_bounds = [lambda z, y: y - z, lambda z, y: y + z]
    # y_bounds = [lambda y: 0, lambda y: y]
    # x_bounds = [0, 1]