"""Unit Test module for src.parse.focus"""
import pytest
from src.parse import focus


@pytest.fixture
def idle():
    return """idle=           [X86]
            Format: idle=poll, idle=halt, idle=nomwait
            Poll forces a polling idle loop that can slightly
            improve the performance of waking up a idle CPU, but
            will use a lot of power and make the system run hot.
            Not recommended.
            idle=halt: Halt is forced to be used for CPU idle.
            In such case C2/C3 won't be used again.
            idle=nomwait: Disable mwait for CPU C-states"""


@pytest.fixture
def kvm_intel_ept():
    return """kvm-intel.ept=  [KVM,Intel] Disable extended page tables
            (virtualized MMU) support on capable Intel chips.
            Default is 1 (enabled)"""


@pytest.fixture
def filter_non_indented_step():
    return focus.FilterNonIndented()


@pytest.fixture
def focus_first_word_step():
    return focus.FocusFirstWord()


@pytest.fixture
def separate_module_and_param_name_step():
    return focus.SeparateModuleAndParamName(module_param_separator=':')


class TestStepFilterNonIndented:

    def test_parsable_on_positive(self, filter_non_indented_step, idle):
        assert filter_non_indented_step.is_parsable(idle)

    def test_parsable_on_empty_string(self, filter_non_indented_step):
        assert not filter_non_indented_step.is_parsable("")

    def test_parsable_on_empty_list(self, filter_non_indented_step):
        assert not filter_non_indented_step.is_parsable([])

    def test_parsable_on_none(self, filter_non_indented_step):
        assert not filter_non_indented_step.is_parsable(None)

    def test_filters_single(self, filter_non_indented_step, idle):
        result = filter_non_indented_step.parse(idle)
        assert len(result) == 1
        assert result[0] == idle.splitlines()[0]

    def test_filter_multiple(self, filter_non_indented_step, idle, kvm_intel_ept):
        full_input = "\n".join([idle, kvm_intel_ept])
        result = filter_non_indented_step.parse(full_input)
        assert len(result) == 2
        assert result[0].startswith('idle')
        assert result[1].startswith('kvm-intel.ept')


class TestFocusFirstWord:

    def test_parsable_on_positive_empty(self, focus_first_word_step):
        assert focus_first_word_step.is_parsable([])

    def test_parsable_on_positive(self, focus_first_word_step):
        assert focus_first_word_step.is_parsable("idle=           [X86]")

    def test_parsable_on_negative_none(self, focus_first_word_step):
        assert not focus_first_word_step.is_parsable(None)

    def test_parsable_on_negative_indented(self, focus_first_word_step, idle):
        idle_indented = "\t" + idle
        assert not focus_first_word_step.is_parsable(idle_indented)

    def test_focus_single(self, focus_first_word_step, kvm_intel_ept):
        filtered_line = kvm_intel_ept.splitlines()[0]
        result = focus_first_word_step.parse(filtered_line)
        assert len(result) == 1
        assert result[0] == "kvm-intel.ept"

    def test_focus_multiple(self, focus_first_word_step, idle, kvm_intel_ept):
        filtered_lines = [kvm_intel_ept.splitlines()[0], idle.splitlines()[0]]
        result = focus_first_word_step.parse(filtered_lines)
        assert len(result) == 2
        assert result[0] == 'kvm-intel.ept'
        assert result[1] == 'idle'


class TestSeperateModuleAndParamName:

    def test_separate_single_core(self, separate_module_and_param_name_step):
        result = separate_module_and_param_name_step.parse("idle")
        assert len(result) == 1
        assert result[0] == "core:idle"

    def test_separate_single_module(self, separate_module_and_param_name_step):
        result = separate_module_and_param_name_step.parse("kvm-intel.ept")
        assert len(result) == 1
        assert result[0] == "kvm-intel:ept"

    def test_separate_multiple(self, separate_module_and_param_name_step):
        result = separate_module_and_param_name_step.parse(["idle", 'kvm-intel.ept'])
        assert len(result) == 2
        assert result[0] == "core:idle"
        assert result[1] == "kvm-intel:ept"

    def test_as_record_none_if_not_parsed(self, separate_module_and_param_name_step):
        assert separate_module_and_param_name_step.as_record() is None

    def test_as_record_single(self, separate_module_and_param_name_step):
        separate_module_and_param_name_step.parse('idle')
        record = separate_module_and_param_name_step.as_record()
        assert record is not None
        assert record[0].parameter_name == 'idle'
        assert record[0].module_name == 'core'

    def test_as_record_list(self, separate_module_and_param_name_step):
        separate_module_and_param_name_step.parse(['idle', 'kvm-intel.ept'])
        record = separate_module_and_param_name_step.as_record()
        assert len(record) == 2
        assert record[0].parameter_name == 'idle'
        assert record[1].parameter_name == 'ept'
        assert record[1].module_name == 'kvm-intel'

    def test_as_record_empty(self, separate_module_and_param_name_step):
        separate_module_and_param_name_step.parse([])
        record = separate_module_and_param_name_step.as_record()
        assert record == []
