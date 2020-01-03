import scipy.io as sio

tri = sio.loadmat('visualize/tri.mat')['tri']
print('tri.shape: ' + str(tri.shape))


def dump_to_ply(vertex, wfp, tri=tri):
    header = """ply
    format ascii 1.0
    element vertex {}
    property float x
    property float y
    property float z
    element face {}
    property list uchar int vertex_indices
    end_header"""

    n_vertex = vertex.shape[0]
    print('n_vertex: ' + str(n_vertex))
    n_face = tri.shape[1]
    header = header.format(n_vertex, n_face)

    with open(wfp, 'w') as f:
        f.write(header + '\n')
        for i in range(n_vertex):
            x, y, z = vertex[i]
            f.write('{:.4f} {:.4f} {:.4f}\n'.format(x, y, z))
        for i in range(n_face):
            idx1, idx2, idx3 = tri[:, i]
            f.write('3 {} {} {}\n'.format(idx1 - 1, idx2 - 1, idx3 - 1))
    print('Dump tp {}'.format(wfp))


def write_obj_with_colors(obj_name, vertices, colors):
    triangles = tri.copy()  # meshlab start with 1

    if obj_name.split('.')[-1] != 'obj':
        obj_name = obj_name + '.obj'

    # write obj
    with open(obj_name, 'w') as f:
        # write vertices & colors
        for i in range(vertices.shape[0]):
            s = 'v {:.4f} {:.4f} {:.4f} {} {} {}\n'.format(vertices[i, 1], vertices[i, 0], vertices[i, 2], colors[i, 0],
                                                           colors[i, 1], colors[i, 2])
            f.write(s)

        # write f: ver ind/ uv ind
        for i in range(triangles.shape[1]):
            s = 'f {} {} {}\n'.format(triangles[0, i], triangles[1, i], triangles[2, i])
            f.write(s)
