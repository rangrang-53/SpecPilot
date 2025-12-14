"""Dummy Workflow - 더미 구현"""
from backend.domain.models.state import RequirementState
from backend.domain.agents.consultant_agent import consultant_agent
from backend.domain.agents.judge_agent import judge_agent
from backend.domain.agents.writer_agent import writer_agent


class DummyWorkflow:
    """
    다중 에이전트 워크플로우 더미 구현

    Consultant → Judge → (conditional) Writer
    """

    def __init__(self):
        """워크플로우 초기화"""
        self.consultant_agent = consultant_agent
        self.judge_agent = judge_agent
        self.writer_agent = writer_agent

    def run(self, state: RequirementState) -> RequirementState:
        """
        워크플로우 실행

        Args:
            state: 현재 요구사항 상태

        Returns:
            업데이트된 요구사항 상태
        """
        # 1. Consultant 실행 (항상)
        state = self.consultant_agent(state)

        # 2. Judge 실행 (항상)
        state = self.judge_agent(state)

        # 3. Writer 실행 (조건부: is_complete가 True일 때만)
        if state.is_complete:
            state = self.writer_agent(state)

        # 4. iteration_count 증가
        state.iteration_count += 1

        return state
