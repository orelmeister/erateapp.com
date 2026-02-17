"""
Link Architect Sub-Agent for erateapp.com
==========================================
Internal linking specialist for silo architecture and link equity distribution.

This agent is delegated tasks by the SEO Orchestrator and specializes in:
- Silo structure planning
- Internal link mapping and optimization
- Anchor text strategy
- Link equity distribution
- Orphan page identification
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum


class LinkType(Enum):
    CONTEXTUAL = "contextual"     # Within body content
    NAVIGATION = "navigation"     # Header/footer nav
    CTA = "cta"                   # Call-to-action button
    RELATED = "related"           # Related articles section
    BREADCRUMB = "breadcrumb"     # Breadcrumb navigation


class SiloType(Enum):
    SERVICES = "services"         # Money pages
    AUDIENCE = "audience"         # Segment landing pages
    RESOURCES = "resources"       # Informational/TOFU content
    BLOG = "blog"                 # Blog posts


@dataclass
class InternalLink:
    """Represents an internal link with full context."""
    source_url: str
    destination_url: str
    anchor_text: str
    link_type: LinkType
    priority: str  # critical, high, medium, low
    context: str   # Where in the content to place
    silo: SiloType


@dataclass
class SiloStructure:
    """Represents a content silo structure."""
    name: str
    silo_type: SiloType
    hub_page: str
    spoke_pages: List[str]
    internal_links: List[InternalLink]


class LinkArchitect:
    """
    Link Architect sub-agent for internal linking operations.
    
    Expertise areas:
    - Silo structure planning
    - Internal link mapping
    - Anchor text optimization
    - Link equity distribution
    - Orphan page prevention
    """
    
    def __init__(self):
        self.domain = "erateapp.com"
        self.silos: List[SiloStructure] = []
        self.all_links: List[InternalLink] = []
        self._initialize_silo_structure()
        self._initialize_link_map()
    
    def _initialize_silo_structure(self):
        """Initialize the three main content silos."""
        self.silos = [
            SiloStructure(
                name="Services Silo",
                silo_type=SiloType.SERVICES,
                hub_page="/services/",
                spoke_pages=[
                    "/services/e-rate-application-management",
                    "/services/e-rate-appeals",
                    "/services/form-470-filing",
                    "/services/form-471-filing",
                    "/services/pia-review-support"
                ],
                internal_links=[]
            ),
            SiloStructure(
                name="Audience Silo",
                silo_type=SiloType.AUDIENCE,
                hub_page="/",
                spoke_pages=[
                    "/schools/",
                    "/libraries/",
                    "/charter-schools/"
                ],
                internal_links=[]
            ),
            SiloStructure(
                name="Resources Silo",
                silo_type=SiloType.RESOURCES,
                hub_page="/guides/",
                spoke_pages=[
                    "/guides/what-is-e-rate/",
                    "/guides/e-rate-eligibility-calculator/",
                    "/guides/e-rate-deadlines-2026/"
                ],
                internal_links=[]
            ),
            SiloStructure(
                name="Blog Silo",
                silo_type=SiloType.BLOG,
                hub_page="/blog/",
                spoke_pages=[
                    "/blog/common-e-rate-mistakes/",
                    "/blog/fy2026-e-rate-deadlines/",
                    "/blog/calculate-e-rate-discount/",
                    "/blog/e-rate-charter-schools/",
                    "/blog/e-rate-application-denied/",
                    "/blog/e-rate-category-1-vs-category-2/"
                ],
                internal_links=[]
            )
        ]
    
    def _initialize_link_map(self):
        """Initialize the complete internal link map."""
        self.all_links = [
            # Homepage links OUT
            InternalLink(
                source_url="/",
                destination_url="/services/e-rate-appeals",
                anchor_text="E-Rate appeal services",
                link_type=LinkType.CONTEXTUAL,
                priority="high",
                context="Services section or problem section",
                silo=SiloType.SERVICES
            ),
            InternalLink(
                source_url="/",
                destination_url="/schools/",
                anchor_text="e-rate for schools",
                link_type=LinkType.CONTEXTUAL,
                priority="high",
                context="Hero section or audience selector",
                silo=SiloType.AUDIENCE
            ),
            InternalLink(
                source_url="/",
                destination_url="/libraries/",
                anchor_text="e-rate for libraries",
                link_type=LinkType.CONTEXTUAL,
                priority="high",
                context="Audience selector section",
                silo=SiloType.AUDIENCE
            ),
            InternalLink(
                source_url="/",
                destination_url="/guides/what-is-e-rate/",
                anchor_text="what is E-Rate",
                link_type=LinkType.CONTEXTUAL,
                priority="medium",
                context="FAQ or educational section",
                silo=SiloType.RESOURCES
            ),
            InternalLink(
                source_url="/",
                destination_url="/guides/e-rate-deadlines-2026/",
                anchor_text="2026 E-Rate deadlines",
                link_type=LinkType.CTA,
                priority="high",
                context="Urgency banner",
                silo=SiloType.RESOURCES
            ),
            
            # Schools page links OUT
            InternalLink(
                source_url="/schools/",
                destination_url="/services/form-471-filing",
                anchor_text="Form 471 filing assistance",
                link_type=LinkType.CONTEXTUAL,
                priority="high",
                context="Application process section",
                silo=SiloType.SERVICES
            ),
            InternalLink(
                source_url="/schools/",
                destination_url="/guides/e-rate-eligibility-calculator/",
                anchor_text="check your discount rate",
                link_type=LinkType.CONTEXTUAL,
                priority="high",
                context="Eligibility section",
                silo=SiloType.RESOURCES
            ),
            InternalLink(
                source_url="/schools/",
                destination_url="/services/e-rate-appeals",
                anchor_text="appeal denied funding",
                link_type=LinkType.CONTEXTUAL,
                priority="medium",
                context="Problem/pain point section",
                silo=SiloType.SERVICES
            ),
            
            # Libraries page links OUT
            InternalLink(
                source_url="/libraries/",
                destination_url="/services/e-rate-application-management",
                anchor_text="complete application management",
                link_type=LinkType.CONTEXTUAL,
                priority="high",
                context="Services mention",
                silo=SiloType.SERVICES
            ),
            InternalLink(
                source_url="/libraries/",
                destination_url="/guides/what-is-e-rate/",
                anchor_text="learn about the E-Rate program",
                link_type=LinkType.CONTEXTUAL,
                priority="medium",
                context="Intro section",
                silo=SiloType.RESOURCES
            ),
            
            # Charter schools page links OUT
            InternalLink(
                source_url="/charter-schools/",
                destination_url="/services/form-470-filing",
                anchor_text="Form 470 filing help",
                link_type=LinkType.CONTEXTUAL,
                priority="high",
                context="Competitive bidding section",
                silo=SiloType.SERVICES
            ),
            InternalLink(
                source_url="/charter-schools/",
                destination_url="/guides/e-rate-eligibility-calculator/",
                anchor_text="calculate your discount",
                link_type=LinkType.CONTEXTUAL,
                priority="high",
                context="Eligibility section",
                silo=SiloType.RESOURCES
            ),
            
            # Guide pages links OUT
            InternalLink(
                source_url="/guides/what-is-e-rate/",
                destination_url="/services/e-rate-application-management",
                anchor_text="professional E-Rate management",
                link_type=LinkType.CTA,
                priority="high",
                context="CTA section at end",
                silo=SiloType.SERVICES
            ),
            InternalLink(
                source_url="/guides/what-is-e-rate/",
                destination_url="/schools/",
                anchor_text="schools eligible for E-Rate",
                link_type=LinkType.CONTEXTUAL,
                priority="medium",
                context="Eligibility section",
                silo=SiloType.AUDIENCE
            ),
            InternalLink(
                source_url="/guides/what-is-e-rate/",
                destination_url="/libraries/",
                anchor_text="libraries eligible for E-Rate",
                link_type=LinkType.CONTEXTUAL,
                priority="medium",
                context="Eligibility section",
                silo=SiloType.AUDIENCE
            ),
            
            # Eligibility calculator links OUT
            InternalLink(
                source_url="/guides/e-rate-eligibility-calculator/",
                destination_url="/services/form-471-filing",
                anchor_text="start your Form 471 application",
                link_type=LinkType.CTA,
                priority="high",
                context="Post-calculation CTA",
                silo=SiloType.SERVICES
            ),
            
            # Deadlines page links OUT
            InternalLink(
                source_url="/guides/e-rate-deadlines-2026/",
                destination_url="/services/form-470-filing",
                anchor_text="Form 470 filing service",
                link_type=LinkType.CONTEXTUAL,
                priority="high",
                context="October deadline section",
                silo=SiloType.SERVICES
            ),
            InternalLink(
                source_url="/guides/e-rate-deadlines-2026/",
                destination_url="/services/form-471-filing",
                anchor_text="Form 471 filing experts",
                link_type=LinkType.CONTEXTUAL,
                priority="high",
                context="January deadline section",
                silo=SiloType.SERVICES
            ),
            
            # Service pages inter-linking (process flow)
            InternalLink(
                source_url="/services/form-470-filing",
                destination_url="/services/form-471-filing",
                anchor_text="Form 471 filing",
                link_type=LinkType.CONTEXTUAL,
                priority="high",
                context="Process continuation section",
                silo=SiloType.SERVICES
            ),
            InternalLink(
                source_url="/services/form-471-filing",
                destination_url="/services/pia-review-support",
                anchor_text="PIA review preparation",
                link_type=LinkType.CONTEXTUAL,
                priority="high",
                context="What happens next section",
                silo=SiloType.SERVICES
            ),
            InternalLink(
                source_url="/services/pia-review-support",
                destination_url="/services/e-rate-appeals",
                anchor_text="appeal support if needed",
                link_type=LinkType.CONTEXTUAL,
                priority="medium",
                context="If issues arise section",
                silo=SiloType.SERVICES
            ),
            
            # Appeals page context link
            InternalLink(
                source_url="/services/e-rate-appeals",
                destination_url="/guides/what-is-e-rate/",
                anchor_text="E-Rate program requirements",
                link_type=LinkType.CONTEXTUAL,
                priority="low",
                context="Context for why denials happen",
                silo=SiloType.RESOURCES
            ),
        ]
    
    def execute_task(self, task: str, context: Dict) -> Dict:
        """
        Execute a delegated linking task.
        
        Args:
            task: The task type to execute
            context: Additional context for the task
            
        Returns:
            Dict containing task results
        """
        task_handlers = {
            "get_silo_structure": self.get_silo_structure,
            "get_link_map": self.get_link_map,
            "audit_internal_links": self.audit_internal_links,
            "get_page_links": self.get_page_links,
            "find_orphan_pages": self.find_orphan_pages,
            "get_anchor_recommendations": self.get_anchor_recommendations
        }
        
        handler = task_handlers.get(task)
        if handler:
            return handler(context)
        else:
            return {"error": f"Unknown task: {task}"}
    
    def get_silo_structure(self, context: Dict) -> Dict:
        """Return the complete silo structure."""
        return {
            "silos": [
                {
                    "name": silo.name,
                    "type": silo.silo_type.value,
                    "hub_page": silo.hub_page,
                    "spoke_pages": silo.spoke_pages,
                    "total_pages": len(silo.spoke_pages) + 1
                }
                for silo in self.silos
            ],
            "total_silos": len(self.silos),
            "total_pages": sum(len(s.spoke_pages) + 1 for s in self.silos)
        }
    
    def get_link_map(self, context: Dict) -> Dict:
        """Return the complete internal link map."""
        return {
            "links": [
                {
                    "source": link.source_url,
                    "destination": link.destination_url,
                    "anchor_text": link.anchor_text,
                    "type": link.link_type.value,
                    "priority": link.priority,
                    "context": link.context,
                    "silo": link.silo.value
                }
                for link in self.all_links
            ],
            "total_links": len(self.all_links),
            "by_priority": {
                "critical": len([l for l in self.all_links if l.priority == "critical"]),
                "high": len([l for l in self.all_links if l.priority == "high"]),
                "medium": len([l for l in self.all_links if l.priority == "medium"]),
                "low": len([l for l in self.all_links if l.priority == "low"])
            }
        }
    
    def audit_internal_links(self, context: Dict) -> Dict:
        """Audit the internal link structure for issues."""
        all_pages: Set[str] = set()
        pages_with_incoming: Set[str] = set()
        pages_with_outgoing: Set[str] = set()
        
        # Collect all pages
        for silo in self.silos:
            all_pages.add(silo.hub_page)
            all_pages.update(silo.spoke_pages)
        
        # Track incoming/outgoing links
        for link in self.all_links:
            pages_with_outgoing.add(link.source_url)
            pages_with_incoming.add(link.destination_url)
        
        orphan_pages = all_pages - pages_with_incoming
        dead_end_pages = all_pages - pages_with_outgoing
        
        return {
            "total_pages": len(all_pages),
            "total_links": len(self.all_links),
            "average_links_per_page": round(len(self.all_links) / len(all_pages), 2) if all_pages else 0,
            "orphan_pages": list(orphan_pages),
            "dead_end_pages": list(dead_end_pages),
            "issues": {
                "orphan_count": len(orphan_pages),
                "dead_end_count": len(dead_end_pages)
            },
            "recommendations": [
                f"Add incoming links to: {page}" for page in orphan_pages
            ] + [
                f"Add outgoing links from: {page}" for page in dead_end_pages
            ]
        }
    
    def get_page_links(self, context: Dict) -> Dict:
        """Get all links for a specific page."""
        page_url = context.get("page_url", "/")
        
        incoming = [l for l in self.all_links if l.destination_url == page_url]
        outgoing = [l for l in self.all_links if l.source_url == page_url]
        
        return {
            "page": page_url,
            "incoming_links": [
                {
                    "from": l.source_url,
                    "anchor_text": l.anchor_text,
                    "type": l.link_type.value
                }
                for l in incoming
            ],
            "outgoing_links": [
                {
                    "to": l.destination_url,
                    "anchor_text": l.anchor_text,
                    "type": l.link_type.value,
                    "context": l.context
                }
                for l in outgoing
            ],
            "incoming_count": len(incoming),
            "outgoing_count": len(outgoing)
        }
    
    def find_orphan_pages(self, context: Dict) -> Dict:
        """Find pages without incoming internal links."""
        audit = self.audit_internal_links(context)
        return {
            "orphan_pages": audit["orphan_pages"],
            "count": audit["issues"]["orphan_count"],
            "fix_recommendations": [
                {
                    "page": page,
                    "suggested_source": "/",  # Link from homepage as fallback
                    "suggested_anchor": page.strip('/').split('/')[-1].replace('-', ' ').title()
                }
                for page in audit["orphan_pages"]
            ]
        }
    
    def get_anchor_recommendations(self, context: Dict) -> Dict:
        """Get anchor text recommendations for a destination URL."""
        destination = context.get("destination_url")
        
        existing_anchors = [
            l.anchor_text for l in self.all_links 
            if l.destination_url == destination
        ]
        
        # Generate alternative anchors based on URL
        url_parts = destination.strip('/').split('/')
        page_name = url_parts[-1] if url_parts else "home"
        
        alternatives = []
        if "form-470" in page_name:
            alternatives = ["Form 470 help", "470 filing service", "competitive bidding assistance"]
        elif "form-471" in page_name:
            alternatives = ["Form 471 assistance", "471 application help", "form 471 experts"]
        elif "appeals" in page_name:
            alternatives = ["E-Rate appeal help", "funding denial appeal", "USAC appeal service"]
        elif "schools" in page_name:
            alternatives = ["school E-Rate funding", "K-12 E-Rate", "school technology grants"]
        elif "libraries" in page_name:
            alternatives = ["library E-Rate", "public library funding", "library broadband grants"]
        
        return {
            "destination": destination,
            "existing_anchors": existing_anchors,
            "alternative_suggestions": alternatives,
            "best_practice": "Vary anchor text while keeping it keyword-rich and natural"
        }


# =========================================================================
# EXAMPLE USAGE
# =========================================================================

if __name__ == "__main__":
    architect = LinkArchitect()
    
    # Get silo structure
    silos = architect.get_silo_structure({})
    print("Silo Structure:")
    for silo in silos["silos"]:
        print(f"\n  {silo['name']} ({silo['type']})")
        print(f"    Hub: {silo['hub_page']}")
        print(f"    Spokes: {silo['spoke_pages']}")
    
    # Audit links
    print("\n\nLink Audit:")
    audit = architect.audit_internal_links({})
    print(f"  Total pages: {audit['total_pages']}")
    print(f"  Total links: {audit['total_links']}")
    print(f"  Avg links/page: {audit['average_links_per_page']}")
    
    if audit["orphan_pages"]:
        print(f"  ⚠️ Orphan pages: {audit['orphan_pages']}")
    
    # Get links for homepage
    print("\n\nHomepage Links:")
    home_links = architect.get_page_links({"page_url": "/"})
    print(f"  Outgoing: {home_links['outgoing_count']}")
    for link in home_links["outgoing_links"]:
        print(f"    → {link['to']} (anchor: '{link['anchor_text']}')")
