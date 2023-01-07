import ast


class ConvertSideEffect(ast.NodeTransformer):
    def visit_Lambda(self, node):
        if isinstance(node.body, ast.Compare):
            return ast.Assert(
                test=node.body,
                msg=ast.JoinedStr(
                    values=[
                        ast.Constant(value="left="),
                        ast.FormattedValue(value=node.body.left, conversion=-1),
                        ast.Constant(value=" right="),
                        ast.FormattedValue(
                            value=node.body.comparators[0], conversion=-1
                        ),
                    ]
                ),
            )
        else:
            return ast.Assert(
                test=node.body,
                msg=ast.JoinedStr(
                    values=[
                        ast.Constant(value=ast.unparse(node.body)),
                        ast.Constant(value=" is False."),
                    ]
                ),
            )
