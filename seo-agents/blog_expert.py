"""
Blog Expert Sub-Agent for erateapp.com
======================================
Specialized agent for blog content creation, optimization, and internal linking.

This agent is delegated tasks by the SEO Orchestrator and specializes in:
- Blog post planning and outlines
- Content optimization for SEO
- Internal link placement within blog content
- Title/meta optimization for blog posts
- Content calendar execution
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from enum import Enum


class ContentIntent(Enum):
    """Search intent categories for blog content."""
    INFORMATIONAL = "informational"  # How-to, What is, Guide
    COMMERCIAL = "commercial"        # Best, Review, Comparison
    TRANSACTIONAL = "transactional"  # Buy, Hire, Get Started
    NAVIGATIONAL = "navigational"    # Brand searches


class ContentPriority(Enum):
    """Priority levels for content creation."""
    CRITICAL = "critical"   # Must publish within 1 week
    HIGH = "high"           # Publish within 2 weeks
    MEDIUM = "medium"       # Publish within 1 month
    LOW = "low"             # Nice to have


@dataclass
class BlogPost:
    """Represents a planned or published blog post."""
    title: str
    slug: str
    primary_keyword: str
    secondary_keywords: List[str]
    search_intent: ContentIntent
    priority: ContentPriority
    word_count_target: int
    meta_description: str
    outline: List[Dict[str, str]]  # {"heading": "H2 text", "content_notes": "..."}
    internal_links: List[Dict[str, str]]  # {"anchor_text": "...", "destination": "..."}
    publish_date: Optional[str] = None
    author: str = "SkyRate Team"


@dataclass
class InternalLinkRecommendation:
    """Recommendation for placing an internal link in blog content."""
    anchor_text: str
    destination_url: str
    context_sentence: str
    link_type: str  # contextual, cta, related-reading


class BlogExpert:
    """
    Blog Expert sub-agent for blog-specific SEO operations.
    
    Expertise areas:
    - Blog content planning and outlines
    - SEO-optimized title and meta writing
    - Internal link strategy for blogs
    - Content calendar management
    """
    
    def __init__(self):
        self.industry = "SkyRate"
        self.target_domain = "erateapp.com"
        self.blog_base_url = "/blog/"
        self.posts: List[BlogPost] = []
        self._initialize_priority_posts()
        
    def _initialize_priority_posts(self):
        """Initialize the 6 priority blog posts for link equity building."""
        self.posts = [
            BlogPost(
                title="10 Common E-Rate Mistakes That Get Applications Denied",
                slug="common-e-rate-mistakes",
                primary_keyword="e-rate application mistakes",
                secondary_keywords=["e-rate denial reasons", "e-rate application errors", "why e-rate denied"],
                search_intent=ContentIntent.INFORMATIONAL,
                priority=ContentPriority.CRITICAL,
                word_count_target=2500,
                meta_description="Avoid these 10 costly E-Rate mistakes that lead to denied funding. Learn from 25+ years of experience helping schools secure millions in E-Rate.",
                outline=[
                    {"heading": "Why E-Rate Applications Get Denied", "content_notes": "Statistics on denial rates, common patterns"},
                    {"heading": "Mistake #1: Missing Form 470 Competitive Bidding Requirements", "content_notes": "28-day rule, proper posting"},
                    {"heading": "Mistake #2: Incorrect Entity Eligibility Status", "content_notes": "NCES database matching"},
                    {"heading": "Mistake #3: Selecting Wrong Discount Rate", "content_notes": "Free lunch calculation errors"},
                    {"heading": "Mistake #4: Requesting Ineligible Services", "content_notes": "Cat 1 vs Cat 2 confusion"},
                    {"heading": "Mistake #5: Missing Documentation Requirements", "content_notes": "Technology plan, board approval"},
                    {"heading": "Mistake #6: Incorrect Cost Allocation", "content_notes": "Split-funded services"},
                    {"heading": "Mistake #7: Late Invoicing", "content_notes": "Invoice deadline requirements"},
                    {"heading": "Mistake #8: SPIN Changes Not Tracked", "content_notes": "Vendor SPIN verification"},
                    {"heading": "Mistake #9: PIA Response Delays", "content_notes": "15-day response requirement"},
                    {"heading": "Mistake #10: Not Seeking Expert Help", "content_notes": "ROI of consulting"},
                    {"heading": "How to Protect Your Funding", "content_notes": "CTA to services"},
                ],
                internal_links=[
                    {"anchor_text": "E-Rate application management", "destination": "/services/e-rate-application-management"},
                    {"anchor_text": "appeal denied E-Rate funding", "destination": "/services/e-rate-appeals"},
                    {"anchor_text": "Form 470 filing assistance", "destination": "/services/form-470-filing"},
                    {"anchor_text": "what is the E-Rate program", "destination": "/guides/what-is-e-rate/"},
                ]
            ),
            BlogPost(
                title="FY2026 E-Rate Timeline: Every Deadline You Cannot Miss",
                slug="fy2026-e-rate-deadlines",
                primary_keyword="e-rate deadlines 2026",
                secondary_keywords=["FY2026 e-rate timeline", "form 471 deadline 2026", "e-rate filing window"],
                search_intent=ContentIntent.INFORMATIONAL,
                priority=ContentPriority.CRITICAL,
                word_count_target=2000,
                meta_description="Complete FY2026 E-Rate deadline calendar. Form 470, Form 471, invoice deadlines, and PIA response windows all in one guide.",
                outline=[
                    {"heading": "Understanding E-Rate Funding Year 2026", "content_notes": "What FY2026 covers"},
                    {"heading": "Pre-Application Phase (July-October 2025)", "content_notes": "Planning and prep"},
                    {"heading": "Form 470 Filing Window", "content_notes": "October opening, 28-day minimum"},
                    {"heading": "Form 471 Application Window (January-March 2026)", "content_notes": "Key dates"},
                    {"heading": "PIA Review Period (April-June 2026)", "content_notes": "Response deadlines"},
                    {"heading": "Funding Commitment Letters", "content_notes": "Wave timing"},
                    {"heading": "Service Delivery Period (July 2026-June 2027)", "content_notes": "Implementation"},
                    {"heading": "Invoice Deadlines", "content_notes": "BEAR vs SPI, 120-day rule"},
                    {"heading": "Download: FY2026 E-Rate Calendar PDF", "content_notes": "Lead magnet"},
                ],
                internal_links=[
                    {"anchor_text": "Form 470 filing service", "destination": "/services/form-470-filing"},
                    {"anchor_text": "Form 471 help", "destination": "/services/form-471-filing"},
                    {"anchor_text": "PIA review preparation", "destination": "/services/pia-review-support"},
                    {"anchor_text": "deadline calendar", "destination": "/guides/e-rate-deadlines-2026/"},
                ]
            ),
            BlogPost(
                title="How to Calculate Your School's E-Rate Discount Rate",
                slug="calculate-e-rate-discount",
                primary_keyword="e-rate discount calculator",
                secondary_keywords=["e-rate eligibility calculator", "school e-rate discount rate", "free lunch e-rate"],
                search_intent=ContentIntent.INFORMATIONAL,
                priority=ContentPriority.HIGH,
                word_count_target=1800,
                meta_description="Learn exactly how to calculate your school's E-Rate discount rate using NSLP data. Step-by-step guide with examples + free calculator tool.",
                outline=[
                    {"heading": "What Determines Your E-Rate Discount?", "content_notes": "NSLP percentage overview"},
                    {"heading": "The E-Rate Discount Matrix Explained", "content_notes": "20%-90% range"},
                    {"heading": "Step 1: Find Your School's NSLP Percentage", "content_notes": "Where to get data"},
                    {"heading": "Step 2: Determine Urban vs Rural Status", "content_notes": "Census definitions"},
                    {"heading": "Step 3: Apply the Discount Matrix", "content_notes": "Category 1 vs 2"},
                    {"heading": "District-Wide vs Individual School Discounts", "content_notes": "Calculation methods"},
                    {"heading": "Common Calculation Mistakes to Avoid", "content_notes": "Errors we see"},
                    {"heading": "Use Our Free E-Rate Calculator", "content_notes": "CTA to tool"},
                ],
                internal_links=[
                    {"anchor_text": "E-Rate discount calculator", "destination": "/guides/e-rate-eligibility-calculator/"},
                    {"anchor_text": "e-rate funding for schools", "destination": "/schools/"},
                    {"anchor_text": "application management", "destination": "/services/e-rate-application-management"},
                ]
            ),
            BlogPost(
                title="E-Rate for Charter Schools: Complete Eligibility Guide",
                slug="e-rate-charter-schools",
                primary_keyword="e-rate for charter schools",
                secondary_keywords=["are charter schools e-rate eligible", "charter school technology funding", "charter school e-rate application"],
                search_intent=ContentIntent.INFORMATIONAL,
                priority=ContentPriority.HIGH,
                word_count_target=2200,
                meta_description="Yes, charter schools ARE eligible for E-Rate funding. Learn the specific requirements, application process, and how to maximize your charter school's discount.",
                outline=[
                    {"heading": "Are Charter Schools E-Rate Eligible?", "content_notes": "Answer upfront - YES"},
                    {"heading": "Charter School Eligibility Requirements", "content_notes": "State authorization, etc."},
                    {"heading": "How Charter School Discounts Are Calculated", "content_notes": "NSLP specifics"},
                    {"heading": "Special Considerations for New Charter Schools", "content_notes": "First-year challenges"},
                    {"heading": "Multi-Site Charter Organizations", "content_notes": "Consortium filing"},
                    {"heading": "Category 1 Services for Charter Schools", "content_notes": "Internet, telco"},
                    {"heading": "Category 2 Funding for Technology", "content_notes": "Wi-Fi, firewall, cabling"},
                    {"heading": "Common Charter School E-Rate Mistakes", "content_notes": "What we see"},
                    {"heading": "How We Help Charter Schools", "content_notes": "CTA"},
                ],
                internal_links=[
                    {"anchor_text": "charter schools", "destination": "/charter-schools/"},
                    {"anchor_text": "Form 471 filing help", "destination": "/services/form-471-filing"},
                    {"anchor_text": "check your discount rate", "destination": "/guides/e-rate-eligibility-calculator/"},
                ]
            ),
            BlogPost(
                title="What to Do When Your E-Rate Application is Denied",
                slug="e-rate-application-denied",
                primary_keyword="e-rate application denied",
                secondary_keywords=["e-rate appeal process", "usac appeal", "e-rate funding denial"],
                search_intent=ContentIntent.COMMERCIAL,
                priority=ContentPriority.CRITICAL,
                word_count_target=2000,
                meta_description="E-Rate application denied? Don't give up. Learn the appeal process, common denial reasons, and how our 90%+ appeal success rate can help recover your funding.",
                outline=[
                    {"heading": "Your E-Rate Was Denied - Now What?", "content_notes": "Don't panic, there's hope"},
                    {"heading": "Understanding Your Denial Letter", "content_notes": "Key sections to review"},
                    {"heading": "Common Reasons for E-Rate Denials", "content_notes": "Top 5 reasons"},
                    {"heading": "The USAC Appeal Process Explained", "content_notes": "Timeline and steps"},
                    {"heading": "When to Escalate to the FCC", "content_notes": "Second-level appeals"},
                    {"heading": "Preparing a Winning Appeal", "content_notes": "Documentation needed"},
                    {"heading": "Appeal Deadlines You Cannot Miss", "content_notes": "Critical dates"},
                    {"heading": "Our E-Rate Appeal Success Record", "content_notes": "90%+ win rate"},
                    {"heading": "Get Help With Your Appeal Today", "content_notes": "Strong CTA"},
                ],
                internal_links=[
                    {"anchor_text": "E-Rate appeal help", "destination": "/services/e-rate-appeals"},
                    {"anchor_text": "application management", "destination": "/services/e-rate-application-management"},
                    {"anchor_text": "what is E-Rate", "destination": "/guides/what-is-e-rate/"},
                ]
            ),
            BlogPost(
                title="E-Rate Category 1 vs Category 2: Which Services Qualify?",
                slug="e-rate-category-1-vs-category-2",
                primary_keyword="e-rate category 1 vs category 2",
                secondary_keywords=["e-rate eligible services", "what does e-rate cover", "e-rate service categories"],
                search_intent=ContentIntent.INFORMATIONAL,
                priority=ContentPriority.MEDIUM,
                word_count_target=1800,
                meta_description="Complete guide to E-Rate Category 1 (internet/telecom) vs Category 2 (internal connections). Learn what services qualify and how to maximize both.",
                outline=[
                    {"heading": "The Two Categories of E-Rate Funding", "content_notes": "Overview"},
                    {"heading": "Category 1: Telecommunications & Internet Access", "content_notes": "Services list"},
                    {"heading": "Category 2: Internal Connections", "content_notes": "Equipment, installation"},
                    {"heading": "Category 2 Budget Caps Explained", "content_notes": "$167/student rule"},
                    {"heading": "Services That Don't Qualify", "content_notes": "Common mistakes"},
                    {"heading": "How to Maximize Both Categories", "content_notes": "Strategy"},
                    {"heading": "Planning Your E-Rate Application", "content_notes": "CTA to services"},
                ],
                internal_links=[
                    {"anchor_text": "what is E-Rate", "destination": "/guides/what-is-e-rate/"},
                    {"anchor_text": "Form 470 filing", "destination": "/services/form-470-filing"},
                    {"anchor_text": "Form 471 application", "destination": "/services/form-471-filing"},
                    {"anchor_text": "E-Rate consulting services", "destination": "/"},
                ]
            ),
        ]
    
    def execute_task(self, task: str, context: Dict) -> Dict:
        """
        Execute a delegated blog task.
        
        Args:
            task: The task type to execute
            context: Additional context for the task
            
        Returns:
            Dict containing task results
        """
        task_handlers = {
            "get_priority_posts": self.get_priority_posts,
            "generate_outline": self.generate_blog_outline,
            "get_internal_links": self.get_internal_link_recommendations,
            "optimize_meta": self.optimize_blog_meta,
            "get_content_calendar": self.get_content_calendar,
            "analyze_blog_seo": self.analyze_blog_seo
        }
        
        handler = task_handlers.get(task)
        if handler:
            return handler(context)
        else:
            return {"error": f"Unknown task: {task}"}
    
    def get_priority_posts(self, context: Dict) -> Dict:
        """Return the priority blog posts for initial SEO launch."""
        return {
            "priority_posts": [
                {
                    "title": post.title,
                    "slug": post.slug,
                    "url": f"{self.blog_base_url}{post.slug}/",
                    "primary_keyword": post.primary_keyword,
                    "secondary_keywords": post.secondary_keywords,
                    "priority": post.priority.value,
                    "word_count_target": post.word_count_target,
                    "internal_links": post.internal_links
                }
                for post in self.posts
            ],
            "total_posts": len(self.posts),
            "critical_count": len([p for p in self.posts if p.priority == ContentPriority.CRITICAL]),
            "high_count": len([p for p in self.posts if p.priority == ContentPriority.HIGH])
        }
    
    def generate_blog_outline(self, context: Dict) -> Dict:
        """Generate a detailed outline for a specific blog post."""
        slug = context.get("slug")
        post = next((p for p in self.posts if p.slug == slug), None)
        
        if not post:
            return {"error": f"Post with slug '{slug}' not found"}
        
        return {
            "title": post.title,
            "slug": post.slug,
            "meta_description": post.meta_description,
            "word_count_target": post.word_count_target,
            "outline": post.outline,
            "internal_links": post.internal_links,
            "writing_guidelines": {
                "tone": "Professional but approachable",
                "audience": "School/library administrators, IT directors",
                "cta_placement": "After problems identified, before conclusion",
                "link_density": "1 internal link per 300-500 words"
            }
        }
    
    def get_internal_link_recommendations(self, context: Dict) -> Dict:
        """Get internal link recommendations for a blog post."""
        slug = context.get("slug")
        post = next((p for p in self.posts if p.slug == slug), None)
        
        if not post:
            return {"error": f"Post with slug '{slug}' not found"}
        
        recommendations = []
        for link in post.internal_links:
            recommendations.append(
                InternalLinkRecommendation(
                    anchor_text=link["anchor_text"],
                    destination_url=link["destination"],
                    context_sentence=f"Consider linking '{link['anchor_text']}' to {link['destination']} within contextually relevant paragraph.",
                    link_type="contextual"
                ).__dict__
            )
        
        # Add CTA links
        recommendations.append({
            "anchor_text": "Get expert E-Rate help",
            "destination_url": "/",
            "context_sentence": "Primary CTA at end of article",
            "link_type": "cta"
        })
        
        return {
            "post_slug": slug,
            "recommendations": recommendations,
            "link_count": len(recommendations)
        }
    
    def optimize_blog_meta(self, context: Dict) -> Dict:
        """Optimize title tag and meta description for a blog post."""
        slug = context.get("slug")
        post = next((p for p in self.posts if p.slug == slug), None)
        
        if not post:
            return {"error": f"Post with slug '{slug}' not found"}
        
        # Generate optimized title (under 60 chars)
        title_options = [
            post.title,  # Original
            f"{post.primary_keyword.title()} | Expert Guide",
            f"{post.primary_keyword.title()} for Schools & Libraries",
        ]
        
        # Pick the best title under 60 chars
        optimized_title = next(
            (t for t in title_options if len(t) <= 60), 
            title_options[0][:57] + "..."
        )
        
        return {
            "slug": slug,
            "optimized_title": optimized_title,
            "character_count": len(optimized_title),
            "meta_description": post.meta_description,
            "meta_char_count": len(post.meta_description),
            "primary_keyword": post.primary_keyword,
            "keyword_in_title": post.primary_keyword.lower() in optimized_title.lower()
        }
    
    def get_content_calendar(self, context: Dict) -> Dict:
        """Generate a content calendar for the priority posts."""
        start_date = datetime.now()
        calendar = []
        
        # Sort by priority
        sorted_posts = sorted(
            self.posts, 
            key=lambda p: ["critical", "high", "medium", "low"].index(p.priority.value)
        )
        
        current_date = start_date
        for post in sorted_posts:
            if post.priority == ContentPriority.CRITICAL:
                days_offset = 7
            elif post.priority == ContentPriority.HIGH:
                days_offset = 14
            else:
                days_offset = 21
            
            publish_date = current_date + timedelta(days=days_offset)
            calendar.append({
                "title": post.title,
                "slug": post.slug,
                "publish_date": publish_date.strftime("%Y-%m-%d"),
                "priority": post.priority.value,
                "word_count": post.word_count_target
            })
            current_date = publish_date
        
        return {
            "calendar": calendar,
            "total_posts": len(calendar),
            "estimated_completion": calendar[-1]["publish_date"] if calendar else None
        }
    
    def analyze_blog_seo(self, context: Dict) -> Dict:
        """Analyze SEO readiness of all planned blog posts."""
        analysis = {
            "total_posts": len(self.posts),
            "posts_by_priority": {
                "critical": [],
                "high": [],
                "medium": [],
                "low": []
            },
            "keyword_coverage": [],
            "internal_link_summary": {
                "total_planned_links": 0,
                "unique_destinations": set()
            }
        }
        
        for post in self.posts:
            priority_key = post.priority.value
            analysis["posts_by_priority"][priority_key].append(post.title)
            analysis["keyword_coverage"].append({
                "keyword": post.primary_keyword,
                "intent": post.search_intent.value,
                "post": post.title
            })
            analysis["internal_link_summary"]["total_planned_links"] += len(post.internal_links)
            for link in post.internal_links:
                analysis["internal_link_summary"]["unique_destinations"].add(link["destination"])
        
        # Convert set to list for JSON serialization
        analysis["internal_link_summary"]["unique_destinations"] = list(
            analysis["internal_link_summary"]["unique_destinations"]
        )
        
        return analysis


# =========================================================================
# EXAMPLE USAGE
# =========================================================================

if __name__ == "__main__":
    expert = BlogExpert()
    
    # Get priority posts
    priority = expert.get_priority_posts({})
    print("Priority Blog Posts:")
    for post in priority["priority_posts"]:
        print(f"  - [{post['priority'].upper()}] {post['title']}")
        print(f"    Keyword: {post['primary_keyword']}")
        print(f"    Links to: {[l['destination'] for l in post['internal_links']]}")
        print()
    
    # Get content calendar
    calendar = expert.get_content_calendar({})
    print("\nContent Calendar:")
    for item in calendar["calendar"]:
        print(f"  {item['publish_date']}: {item['title']}")
