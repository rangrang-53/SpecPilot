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

    def to_markdown(self, srs) -> str:
        """
        SRS 문서를 Markdown 형식으로 변환

        Args:
            srs: SRS 문서 객체 또는 dict

        Returns:
            Markdown 형식 문자열
        """
        # dict인 경우 그대로 사용, 아니면 객체 속성 접근
        if isinstance(srs, dict):
            data = srs
        else:
            # SRSDocument 객체인 경우
            data = srs.model_dump() if hasattr(srs, 'model_dump') else srs.__dict__

        md = []

        # 제목
        md.append(f"# {data.get('project_name', 'Untitled Project')}\n")

        # 개요
        md.append("## 프로젝트 개요\n")
        md.append(f"{data.get('overview', 'N/A')}\n")

        # 기능 요구사항
        md.append("## 기능 요구사항\n")
        for req in data.get('functional_requirements', []):
            md.append(f"### {req.get('id', 'N/A')}: {req.get('title', 'N/A')}\n")
            md.append(f"**우선순위**: {req.get('priority', 'N/A')}\n\n")
            md.append(f"{req.get('description', 'N/A')}\n\n")
            if req.get('tech_suggestions'):
                md.append(f"**기술 제안**: {', '.join(req['tech_suggestions'])}\n\n")

        # 비기능 요구사항
        nfr_list = data.get('non_functional_requirements', [])
        if nfr_list:
            md.append("## 비기능 요구사항\n")
            for nfr in nfr_list:
                md.append(f"- {nfr}\n")
            md.append("\n")

        # 기술 스택
        tech_stack = data.get('tech_stack', [])
        if tech_stack:
            md.append("## 기술 스택\n")
            for tech in tech_stack:
                md.append(f"### {tech.get('category', 'N/A')}\n")
                md.append(f"**기술**: {', '.join(tech.get('technologies', []))}\n\n")
                md.append(f"**선정 이유**: {tech.get('rationale', 'N/A')}\n\n")

        # 테스트 시나리오
        scenarios = data.get('test_scenarios', [])
        if scenarios:
            md.append("## 테스트 시나리오\n")
            for scenario in scenarios:
                md.append(f"### {scenario.get('feature', 'N/A')}: {scenario.get('scenario', 'N/A')}\n")
                md.append(f"- **Given**: {scenario.get('given', 'N/A')}\n")
                md.append(f"- **When**: {scenario.get('when', 'N/A')}\n")
                md.append(f"- **Then**: {scenario.get('then', 'N/A')}\n\n")

        # 가정사항
        assumptions = data.get('assumptions', [])
        if assumptions:
            md.append("## 가정사항\n")
            for assumption in assumptions:
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
