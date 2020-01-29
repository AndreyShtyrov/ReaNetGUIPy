import itertools
import math

import numpy as np
import scipy
import scipy.spatial
from numpy import linalg


def separete_basis(first_part):
    """
    РџСЂРёРЅРёРјР°РµС‚ РЅР° РІС…РѕРґ РЅР°Р±РѕСЂ РІРµРєС‚РѕСЂРѕРІ, Р° Р·Р°С‚РµРј РґРѕСЃС‚СЂР°РёРІР°РµС‚ СЃРёСЃС‚РµРјСѓ РґРѕ Р±Р°Р·РёСЃР° СЃ РїРѕРјРѕС‰СЊСЋ РїСЂРѕС†РµСЃСЃР° Р“СЂР°РјР°-РЁРјРёРґС‚Р°

    :param first_part: РЅР°Р±РѕСЂ РІРµРєС‚РѕСЂРѕРІ РІ РІРёРґРµ РјР°С‚СЂРёС†С‹ nxk, РіРґРµ k - РєРѕР»РёС‡РµСЃС‚РІРѕ РІРµРєС‚РѕСЂРѕРІ, n - РёС… СЂР°Р·РјРµСЂРЅРѕСЃС‚СЊ
    :return: РѕСЂС‚РѕРЅРѕСЂРјРёСЂРѕРІР°РЅРЅС‹Р№ Р±Р°Р·РёСЃ
    """
    np.random.seed(19)  # TODO: don't forget to remove it after debug finished

    n_dims = first_part.shape[0]
    basis = np.zeros((n_dims, n_dims))
    basis[:, : first_part.shape[1]] = first_part
    basis[:, first_part.shape[1]:] = np.random.randn(n_dims, n_dims - first_part.shape[1])
    basis, r = np.linalg.qr(basis)

    return basis


def vector_struct_to_matrix(struct):
    return struct.reshape((-1, 3)).copy()


def matrix_struct_to_vector(struct):
    return struct.ravel().copy()



def calc_numerical_grad(func, q, delta=1e-4):
    numerical_grad = np.zeros(func.n_dims)
    for i in range(func.n_dims):
        e = delta * linalg.eye(func.n_dims, i)
        numerical_grad[i] = 0.5 * (func(q + e) - func(q - e)) / delta
    return numerical_grad


def calc_numerical_hess_from_grad(func, q, delta=1e-4):
    numerical_hess = np.zeros((func.n_dims, func.n_dims))
    for i in range(func.n_dims):
        e = delta * linalg.eye(func.n_dims, i)
        grad_m = func.grad(q - e)
        grad_p = func.grad(q + e)

        numerical_hess[i] = 0.5 * (grad_p - grad_m) / delta

    return numerical_hess


def calc_numerical_hess_from_vals(func, q, delta=1e-4):
    numerical_hess = np.zeros((func.n_dims, func.n_dims))
    for i in range(func.n_dims):
        for j in range(i, func.n_dims):
            e1 = delta * linalg.eye(func.n_dims, i)
            e2 = delta * linalg.eye(func.n_dims, j)

            diff = func(q + e1 + e2) - func(q - e1 + e2) - func(q + e1 - e2) + func(q - e1 - e2)
            numerical_hess[i, j] = 0.25 * diff / delta ** 2
            numerical_hess[j, i] = 0.25 * diff / delta ** 2

    return numerical_hess


def get_arrays_by_components(coords):
    X = np.array([coords[i * 3] for i in range(int(len(coords) / 3))])
    Y = np.array([coords[i * 3 + 1] for i in range(int(len(coords) / 3))])
    Z = np.array([coords[i * 3 + 2] for i in range(int(len(coords) / 3))])
    return X, Y, Z


def calculate_center_of_mass(masses, coords):
    rX, rY, rZ = get_arrays_by_components(coords)

    Xmoment_of_mass = sum(map(lambda x, m: x * m, rX, masses))
    Ymoment_of_mass = sum(map(lambda x, m: x * m, rY, masses))
    Zmonent_of_mass = sum(map(lambda x, m: x * m, rZ, masses))

    sum_of_mass = sum((masses))

    center_of_mass = np.array(
        [Xmoment_of_mass / sum_of_mass, Ymoment_of_mass / sum_of_mass, Zmonent_of_mass / sum_of_mass])

    return center_of_mass


def shift_center_of_coord(coords, new_centor):
    i = 0
    new_coord = np.zeros(len(coords))
    for comp in coords:
        new_coord[i] = comp - new_centor[int(i % 3)]
        i = i + 1
    return new_coord


def calculate_axis_of_inertions(masses, coords):
    rX, rY, rZ = get_arrays_by_components(coords)
    Ixx = sum(map(lambda m, y, z: m * (y * y + z * z), masses, rY, rZ))
    Ixy = sum(map(lambda m, x, y: -m * (x * y), masses, rX, rY))
    Ixz = sum(map(lambda m, x, z: -m * (x * z), masses, rX, rZ))
    Iyx = sum(map(lambda m, y, x: -m * (y * x), masses, rY, rX))
    Iyy = sum(map(lambda m, x, z: m * (x * x + z * z), masses, rX, rZ))
    Iyz = sum(map(lambda m, y, z: -m * (y * z), masses, rY, rZ))
    Izx = sum(map(lambda m, z, x: -m * (z * x), masses, rZ, rX))
    Izy = sum(map(lambda m, z, y: -m * (z * y), masses, rZ, rY))
    Izz = sum(map(lambda m, x, y: m * (x * x + y * y), masses, rX, rY))

    Inertion = np.zeros((3, 3))
    Inertion[0, 0] = Ixx
    Inertion[0, 1] = Ixy
    Inertion[0, 2] = Ixz
    Inertion[1, 0] = Iyx
    Inertion[1, 1] = Iyy
    Inertion[1, 2] = Iyz
    Inertion[2, 0] = Izx
    Inertion[2, 1] = Izy
    Inertion[2, 2] = Izz

    return Inertion


def generate_basis_without_trans_rot(coords, masses):
    n = len(masses) * 3

    mass_center = calculate_center_of_mass(masses, coords)
    coords = shift_center_of_coord(coords, mass_center)
    inert_axis = calculate_axis_of_inertions(masses, coords)
    eigv, X = np.linalg.eigh(inert_axis)

    R = vector_struct_to_matrix(coords)
    P = R.dot(X)

    D = []

    for i in range(3):
        d = np.zeros(n)
        d[i::3] = np.sqrt(masses)
        D.append(d)

    for i in range(3):
        D.append(np.zeros(n))

    for i in range(3):
        D[3][i::3] = (P[:, 1] * X[i, 2] - P[:, 2] * X[i, 1]) * np.sqrt(masses)
        D[4][i::3] = (P[:, 2] * X[i, 0] - P[:, 0] * X[i, 2]) * np.sqrt(masses)
        D[5][i::3] = (P[:, 0] * X[i, 1] - P[:, 1] * X[i, 0]) * np.sqrt(masses)

    result = []
    for i in range(len(D)):
        if D[i][0] is "nan" or np.linalg.norm(D[i]) < 1.0e-12:
            pass
        else:
            result.append(D[i] / np.linalg.norm(D[i]))
    result = np.array(result)
    return separete_basis(np.stack(result, axis=1))[:, len(result):]


def calculate_redundant_mass_coeff(normal_mode):
    factor = sum(map(lambda x: x ** 2, normal_mode))
    factor = 1 / factor
    return factor


# def shell_for_normal_modes(func):
#     def shell(*arg1):
#         masses = arg1[0]  # list
#         coords = arg1[1]  # 1D np.ndarray
#         hessian = arg1[2]  # 2D np.ndarray it should be divided by sqrt(mi * mj)
#         return func(masses, coords, hessian)
#
#     return shell()
#
#
# @shell_for_normal_modes
def get_normal_modes(masses, coords, hessian):
    sqrt_masses = np.zeros(len(masses) * 3)
    for i in range(3):
        sqrt_masses[i::3] = np.sqrt(masses)

    for i, row in enumerate(hessian):
        for j, column in enumerate(row):
            m = sqrt_masses[i] * sqrt_masses[j]
            hessian[i][j] /= m

    new_basis = generate_basis_without_trans_rot(coords, masses)
    hess = new_basis.T.dot(hessian).dot(new_basis)
    eig_v, eig_vectors = np.linalg.eigh(hess)
    normal_modes_not_weight = new_basis.dot(eig_vectors)

    convert_from_au_to_mdyn_per_Ang = 627.5 * 1.889725989 ** 2 * 4184 / (10 ** 5 * 6.022)
    convert_sqrt_mdyn_per_Ang_to_cm = 1302.79

    eig_v = eig_v * convert_from_au_to_mdyn_per_Ang

    factor_list = []
    for i in range(normal_modes_not_weight.shape[1]):
        normal_modes_not_weight[:, i] = normal_modes_not_weight[:, i] / sqrt_masses
        factor = sum(map(lambda x: x ** 2, normal_modes_not_weight[:, i]))
        factor = 1 / factor
        factor_list.append(factor)
        normal_modes_not_weight[:, i] = normal_modes_not_weight[:, i] * math.sqrt(factor)
    normal_modes = normal_modes_not_weight

    freqs = []
    for value in eig_v:
        if value < 0:
            freqs.append(-1 * math.sqrt(-value) * convert_sqrt_mdyn_per_Ang_to_cm)
        else:
            freqs.append(math.sqrt(value) * convert_sqrt_mdyn_per_Ang_to_cm)

    result = np.array(normal_modes)
    return result


if __name__ == '__main__':
    hess_values = [1.39509605E-01, 0.00000000E+00, -3.64759273E-02,  2.28869099E-01,  0.00000000E+00,
               2.13703660E-01, -1.53893725E-01,  0.00000000E+00, -2.19579946E-01,  1.67979543E-01,
               0.00000000E+00,  5.09129244E-02,  0.00000000E+00,  0.00000000E+00, -3.67193735E-02,
               -2.22695085E-01,  0.00000000E+00, -2.03964180E-01,  2.13825024E-01,  0.00000000E+00,
               2.29587286E-01,  1.43841200E-02,  0.00000000E+00, -9.28915274E-03, -1.40858185E-02,
               0.00000000E+00,  8.87006153E-03, -2.98301485E-04,  0.00000000E+00, -1.44369971E-02,
               0.00000000E+00,  0.00000000E+00, -1.41935508E-02,  0.00000000E+00,  0.00000000E+00,
               2.86305480E-02, -6.17401418E-03,  0.00000000E+00, -9.73947945E-03,  5.75492296E-03,
               0.00000000E+00, -2.56231061E-02,  4.19091215E-04,  0.00000000E+00,  3.53625856E-02]
    masses = [1.00784, 1.00784, 1.00784]
    hess_values_iter = iter(hess_values)

    hess = np.zeros((3 * len(masses), 3 * len(masses)))
    for i in range(3 * len(masses)):
        for j in range(0, i + 1):
            hess[i, j] = hess[j, i] = next(hess_values_iter)

    coords = [-0.792995503,      0.000000000,     -0.133455105,
              -0.299868474,      0.000000000,      0.418292785,
              0.505385203,      0.000000000,     -0.301406121]

    charges = [1, 1, 1]
    mode = get_normal_modes(masses, coords, hess)
    print(mode)
    print("++++++++++++++++")
    hess_values1 = [  4.15884077E-01, -8.89834695E-12,  1.80713416E-01, -9.91213900E-12,  1.31633211E-01,
    6.62202670E-02, -2.07942039E-01, -9.63995436E-02, -6.32338127E-02,  2.35860143E-01,
    -1.37582957E-01, -9.03567080E-02, -6.58166055E-02,  1.16991250E-01,  8.63900961E-02,
    -9.02396522E-02, -6.58166055E-02, -3.31101335E-02,  7.67367325E-02,  6.14100120E-02,
    3.29844408E-02, -2.07942039E-01,  9.63995436E-02,  6.32338127E-02, -2.79181044E-02,
    2.05917068E-02,  1.35029198E-02,  2.35860143E-01,  1.37582957E-01, -9.03567080E-02,
    -6.58166055E-02, -2.05917068E-02,  3.96661190E-03,  4.40659355E-03, -1.16991250E-01,
    8.63900961E-02,  9.02396522E-02, -6.58166055E-02, -3.31101335E-02, -1.35029198E-02,
    4.40659354E-03,  1.25692657E-04, -7.67367325E-02,  6.14100119E-02,  3.29844408E-02]

    masses1 = [12.00000, 1.00784, 1.00784]
    coords1 = [-0.11096, 0.07416, -0.6842,
               0.76661, 0.6282, -0.32083,
               - 0.98853, 0.6282, -0.32083]
    hess_values_iter1 = iter(hess_values1)

    hess1 = np.zeros((3 * len(masses1), 3 * len(masses1)))
    for i in range(3 * len(masses1)):
        for j in range(0, i + 1):
            hess1[i, j] = hess1[j, i] = next(hess_values_iter1)


    mode = get_normal_modes(masses1, coords1, hess1)
    print(mode)


class TestLineApp(App):
    def build(self):
        main_path = Path().cwd()
        wid = Test_Widget()
        project = ChProject(main_path)
        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        new_sub = project.add_child()
        Mol1 = MolFrame(new_sub, pos=(200, 300))
        wid.add_widget(Mol1)
        new_sub = project.add_child()
        Mol2 = MolFrame(new_sub, pos=(500, 500))
        wid.add_widget(Mol2)
        line = Bound_pointer(wid.children)
        wid.add_widget(line)
        return root


if __name__ == '__main__':
    TestLineApp().run()



