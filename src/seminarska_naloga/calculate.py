from numpy import array, sum as numpy_sum, sqrt as square_root, delete, insert, max as numpy_max


def electre_method(weights: list[float], data):
    squared_data = data.copy()

    for row in range(squared_data.shape[0]):
        for column in range(squared_data.shape[1]):
            squared_data[row, column] *= squared_data[row, column]

    sum_data = squared_data.transpose()

    normalized_data = [
        square_root(numpy_sum(sum_data[row]))
        for row in range(sum_data.shape[0])
    ]

    for row in range(data.shape[0]):
        for column in range(data.shape[1]):
            data[row, column] /= normalized_data[column]
            data[row, column] *= weights[column]

    weighted_matrix = data.copy()

    def calculate_set_row(set_row: int):
        current_row = weighted_matrix[set_row]
        rest_of_rows = delete(weighted_matrix.copy(), set_row, 0)

        for row in range(rest_of_rows.shape[0]):
            for column in range(rest_of_rows.shape[1]):
                rest_of_rows[
                    row, column] = 1 if current_row[column] >= rest_of_rows[
                        row, column] else 0

        return rest_of_rows

    matrices = [
        calculate_set_row(set_row)
        for set_row in range(weighted_matrix.shape[0])
    ]

    def calculate_interval_matrix(row_index: int):
        current_matrix = matrices[row_index].copy()
        for row in range(current_matrix.shape[0]):
            for column in range(current_matrix.shape[1]):
                current_matrix[
                    row, column] = weights[column] if matrices[row_index][
                        row, column] else 0

        return [
            numpy_sum(current_matrix[row])
            for row in range(current_matrix.shape[0])
        ]

    interval_matrix = array([
        insert(calculate_interval_matrix(m), m, 0)
        for m in range(len(matrices))
    ])

    row_sum = [
        numpy_sum(interval_matrix[row])
        for row in range(interval_matrix.shape[0])
    ]

    m = interval_matrix.shape[0]
    divisor = m * (m - 1)

    c = numpy_sum(row_sum) / divisor

    deteninnine_matrix = interval_matrix.copy()

    for row in range(deteninnine_matrix.shape[0]):
        for column in range(deteninnine_matrix.shape[1]):
            deteninnine_matrix[row][
                column] = 1 if deteninnine_matrix[row][column] >= c else 0

    def calculate_discordance_matrix(set_row: int):
        current_row = weighted_matrix.copy()[set_row]
        rest_of_rows = delete(weighted_matrix.copy(), set_row, 0)

        for row in range(rest_of_rows.shape[0]):
            for column in range(rest_of_rows.shape[1]):
                rest_of_rows[row, column] = abs(current_row[column] -
                                                rest_of_rows[row, column])

        return rest_of_rows

    discordance_matrices = array(
        [calculate_discordance_matrix(m) for m in range(len(weighted_matrix))])

    def calculate_discordance_matrix_indices(matrix_index: int):
        current_matrix = discordance_matrices.copy()[matrix_index]
        zero_one_matrix = matrices.copy()[matrix_index]
        for row in range(current_matrix.shape[0]):
            for column in range(current_matrix.shape[1]):
                zero_one_matrix[row, column] = current_matrix[
                    row, column] if zero_one_matrix[row, column] == 0 else 0

        return [
            numpy_max(zero_one_matrix[row]) / numpy_max(current_matrix[row])
            for row in range(len(current_matrix))
        ]

    discordance_interval_matrix = array([
        insert(calculate_discordance_matrix_indices(m), m, 0)
        for m in range(len(discordance_matrices))
    ])

    discordance_compare_with = numpy_sum(
        numpy_sum(discordance_interval_matrix, 1), 0) / divisor

    dim_copy = discordance_interval_matrix.copy()
    for row in range(discordance_interval_matrix.shape[0]):
        for column in range(discordance_interval_matrix.shape[1]):
            dim_copy[row, column] = 0 if discordance_interval_matrix[
                row, column] > discordance_compare_with else 1

    concordance_row_sums = numpy_sum(interval_matrix, 1)
    concordance_column_sums = numpy_sum(interval_matrix, 0)

    discordance_row_sums = numpy_sum(discordance_interval_matrix, 1)
    discordance_column_sums = numpy_sum(discordance_interval_matrix, 0)

    net_superior_rank = concordance_row_sums - concordance_column_sums
    net_inferior_rank = discordance_row_sums - discordance_column_sums

    return net_superior_rank.tolist(), net_inferior_rank.tolist()
