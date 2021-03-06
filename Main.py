from random import randint


class Generator:
    def __init__(self, num_of_blocks=5, consistently=True):
        self.num_of_blocks = num_of_blocks
        self.consistently = consistently
        self.blocks = list()

    def generate_random_data(self):
        properties = ParamProperties(randint(0, 2), randint(0, 2))
        return properties

    def generate_access_points(self, type_in_out, num_of_access_points):
        access_points_list = list()
        for i in range(num_of_access_points):
            access_point = AccessPoint()
            if (type_in_out):
                access_point.set_type(1)
            else:
                access_point.set_type(0)
            access_point.set_params(self.generate_params_list(randint(1, 4)))
            access_points_list.append(access_point)
        return access_points_list

    def generate_params_list(self, num_of_params):
        params_list = list()
        for i in range(num_of_params):
            params_list.append(self.generate_random_data())
        return params_list

    def generate_initial_scheme(self):
        first_block = Block()
        first_block.set_in(self.generate_access_points(0, randint(1, 3)))
        first_block.set_out(self.generate_access_points(1, randint(1, 3)))
        self.blocks.append(first_block)
        for i in range(self.num_of_blocks - 1):
            block = Block()
            if self.consistently:
                block.set_in(self.blocks[i].get_out_list())
            else:
                block.set_in(self.generate_access_points(1, randint(1, 3)))
            block.set_out(self.generate_access_points(1, randint(1, 3)))
            self.blocks.append(block)

    def generate(self):
        self.generate_initial_scheme()

    def get_blocks(self):
        return self.blocks

def get_next(curr_seq, blocks, used, results):
    local_seq = curr_seq.copy()
    local_used_idxs = used.copy()
    tried_blocks_idxs = list()
    size = len(blocks)
    for i in range(size):
        if i in local_used_idxs or i in tried_blocks_idxs:
            continue

        tried_blocks_idxs.append(i)

        if len(local_seq) == 0:
            local_seq.append(blocks[i])
            local_used_idxs.append(i)
            get_next(local_seq, blocks, local_used_idxs, results)
            local_seq = curr_seq.copy()
            continue

        if is_block_connectable(local_seq[len(local_seq) - 1], blocks[i]):
            local_seq.append(blocks[i])
            local_used_idxs.append(i)
            get_next(local_seq, blocks, local_used_idxs, results)
            local_seq = curr_seq.copy()
            continue
        else:
            if len(local_seq) != 0:
                results.append(local_seq)
    results.append(local_seq)


def is_block_connectable(prev, next):
    if len(prev.out_access_points) != len(next.in_access_points):
        return False

    for i in range(len(prev.out_access_points)):
        prev_block_params = prev.out_access_points[i].params
        next_block_params = next.in_access_points[i].params

        for j in range(len(prev_block_params)):
            if not prev_block_params[j].is_equal(next_block_params[j]):
                return False

        return True


def get_domain_list(blocks):
    domain_list = list()

    for i in range(len(blocks)):
        in_access_points = blocks[i].get_in_list()
        for j in range(len(in_access_points)):
            params = in_access_points[j].get_params()
            for k in range(len(params)):
                find_or_add(domain_list, params[k], 0, in_access_points[j].get_id())

        out_access_points = blocks[i].get_out_list()
        for j in range(len(out_access_points)):
            params = out_access_points[j].get_params()
            for k in range(len(params)):
                find_or_add(domain_list, params[k], 1, out_access_points[j].get_id())

    return domain_list


def find_or_add(domains, params, in_out_type, access_point_id):
    for i in range(len(domains)):
        if domains[i].is_equal(params, in_out_type):
            domains[i].params_list.append(params)
            domains[i].access_points_list_ids.append(access_point_id)
            return True

    domain = Domain(params.type, params.restriction, in_out_type)
    domain.params_list.append(params)
    domain.access_points_list_ids.append(access_point_id)
    domains.append(domain)
    pass


class Block:
    def __init__(self):
        self.in_access_points = list()
        self.out_access_points = list()
        self.access_points_list = list()

    def set_in(self, in_access_points):
        self.in_access_points = in_access_points
        for i in range(len(in_access_points)):
            self.access_points_list.append(in_access_points[i].id)

    def set_out(self, out_access_points):
        self.out_access_points = out_access_points
        for i in range(len(out_access_points)):
            self.access_points_list.append(out_access_points[i].id)

    def get_in_size(self):
        return len(self.in_access_points)

    def get_out_size(self):
        return len(self.out_access_points)

    def get_in_list(self):
        return self.in_access_points

    def get_out_list(self):
        return self.out_access_points


class AccessPoint:
    access_point_id = 0

    def __init__(self):
        self.type_in_out = 0
        self.params = list()
        self.id = AccessPoint.access_point_id
        AccessPoint.access_point_id += 1

    def set_type(self, in_out_type):
        self.type_in_out = in_out_type

    def set_params(self, params):
        self.params = params

    def get_params(self):
        return self.params

    def get_id(self):
        return self.id


class ParamProperties:
    def __init__(self, type, restriction):
        self.type = type
        self.restriction = restriction

    def is_equal(self, params):
        if self.restriction == params.restriction and self.type == params.type:
            return True
        else:
            return False


class Domain(ParamProperties):
    def __init__(self, type, restriction, in_out_type):
        super().__init__(type, restriction)
        self.params_list = list()
        self.in_out_type = in_out_type
        self.access_points_list_ids = list()

    def is_equal(self, properties, in_out_type):
        if self.restriction == properties.restriction and self.type == properties.type and self.in_out_type == in_out_type:
            return True
        else:
            return False

    def add_access_points_id(self, id):
        self.access_points_list_ids.append(id)


if __name__ == "__main__":
    generator = Generator(3, False)
    generator.generate()
    blocks = generator.get_blocks()

    domain_list = get_domain_list(blocks)

    results = list()
    get_next(list(), blocks, list(), results)
    # recursive here

    pass
