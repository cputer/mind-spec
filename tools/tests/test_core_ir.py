import unittest

from tools.core_ir.core_ir import CoreIR
from tools.core_ir.language import BinaryOperation, LanguageConstruct, Literal, Variable
from tools.core_ir.type_system import TensorType, TypeSystem


class TestCoreIRPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.type_system = TypeSystem()
        self.type_system.add_symbol("x", TensorType("f32", (2, 2)))
        self.type_system.add_symbol("y", TensorType("f32", (2, 2)))

    def test_language_construct_to_ir(self) -> None:
        expression = BinaryOperation("Add", Variable("x"), Variable("y"))
        construct = LanguageConstruct(expression, type_system=self.type_system)

        ir = construct.to_ir()
        compiled = ir.compile()

        self.assertIn("%0 = Input", compiled)
        self.assertIn("%1 = Input", compiled)
        self.assertIn("%2 = Add (%0, %1)" , compiled)
        self.assertTrue(compiled.strip().endswith("outputs: %2"))

    def test_scalar_broadcasting(self) -> None:
        self.type_system.add_symbol("bias", TensorType("f32"))
        expression = BinaryOperation("Add", Variable("x"), Variable("bias"))
        construct = LanguageConstruct(expression, type_system=self.type_system)

        ir = construct.to_ir()
        compiled = ir.compile()

        # bias should be materialised once and the result shape should follow x
        self.assertIn("bias", compiled)
        self.assertTrue(compiled.strip().endswith("outputs: %2"))

    def test_type_mismatch_rejected(self) -> None:
        self.type_system.add_symbol("z", TensorType("i32", (2, 2)))
        expression = BinaryOperation("Add", Variable("x"), Variable("z"))

        with self.assertRaises(TypeError):
            LanguageConstruct(expression, type_system=self.type_system).to_ir()


if __name__ == "__main__":
    unittest.main()
