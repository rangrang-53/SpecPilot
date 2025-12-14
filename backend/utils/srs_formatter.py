"""SRS Formatter - SRS 문서 포맷팅"""
import json
from backend.domain.models.srs import SRSDocument


class SRSFormatter:
    """
    SRS 문서를 다양한 포맷으로 변환하는 유틸리티

    JSON → Markdown 변환 지원
    """

    def __init__(self):
        """SRSFormatter 초기화"""
        pass

    def to_markdown(self, srs: SRSDocument) -> str:
        """
        SRS 문서를 Markdown 형식으로 변환

        Args:
            srs: SRS 문서 객체

        Returns:
            Markdown 형식 문자열
        """
        md = []

        # 제목
        md.append(f"# {srs.project_name}\n")

        # 개요
        md.append("## 프로젝트 개요\n")
        md.append(f"{srs.overview}\n")

        # 기능 요구사항
        md.append("## 기능 요구사항\n")
        for req in srs.functional_requirements:
            md.append(f"### {req.id}: {req.title}\n")
            md.append(f"**우선순위**: {req.priority}\n\n")
            md.append(f"{req.description}\n\n")
            if req.tech_suggestions:
                md.append(f"**기술 제안**: {', '.join(req.tech_suggestions)}\n\n")

        # 비기능 요구사항
        if srs.non_functional_requirements:
            md.append("## 비기능 요구사항\n")
            for nfr in srs.non_functional_requirements:
                md.append(f"- {nfr}\n")
            md.append("\n")

        # 기술 스택
        if srs.tech_stack:
            md.append("## 기술 스택\n")
            for tech in srs.tech_stack:
                md.append(f"### {tech.category}\n")
                md.append(f"**기술**: {', '.join(tech.technologies)}\n\n")
                md.append(f"**선정 이유**: {tech.rationale}\n\n")

        # 테스트 시나리오
        if srs.test_scenarios:
            md.append("## 테스트 시나리오\n")
            for scenario in srs.test_scenarios:
                md.append(f"### {scenario.feature}: {scenario.scenario}\n")
                md.append(f"- **Given**: {scenario.given}\n")
                md.append(f"- **When**: {scenario.when}\n")
                md.append(f"- **Then**: {scenario.then}\n\n")

        # 가정사항
        if srs.assumptions:
            md.append("## 가정사항\n")
            for assumption in srs.assumptions:
                md.append(f"- {assumption}\n")

        return "".join(md)

    def json_to_markdown(self, json_str: str) -> str:
        """
        JSON 문자열을 Markdown으로 변환

        Args:
            json_str: JSON 형식의 SRS 문서 문자열

        Returns:
            Markdown 형식 문자열
        """
        data = json.loads(json_str)
        srs = SRSDocument(**data)
        return self.to_markdown(srs)
