"""
Export utilities for E-Rate data
Handles CSV and PDF export with formatting
"""
import csv
import json
from datetime import datetime
from typing import List, Dict, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors


class DataExporter:
    """Export E-Rate data to various formats"""
    
    @staticmethod
    def export_to_csv(data: List[Dict], filename: str, selected_fields: Optional[List[str]] = None) -> bool:
        """
        Export data to CSV file
        
        Args:
            data: List of records to export
            filename: Output filename
            selected_fields: Specific fields to include (None = all fields)
            
        Returns:
            True if successful
        """
        if not data:
            print("✗ No data to export")
            return False
        
        try:
            # Default important fields for E-Rate analysis
            if not selected_fields:
                selected_fields = [
                    'funding_year',
                    'organization_name',
                    'state',
                    'form_471_frn_status_name',
                    'funding_commitment_request',
                    'application_number',
                    'funding_request_number',
                    'nickname',
                    'form_471_service_type_name',
                    'pending_reason',
                    'fcdl_comment_frn',
                    'dis_pct',
                    'organization_entity_type_name'
                ]
            
            # Filter to only fields that exist in data
            available_fields = list(data[0].keys())
            fields_to_export = [f for f in selected_fields if f in available_fields]
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields_to_export, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data)
            
            print(f"✓ Exported {len(data)} records to {filename}")
            print(f"  Fields included: {', '.join(fields_to_export[:5])}{'...' if len(fields_to_export) > 5 else ''}")
            return True
            
        except Exception as e:
            print(f"✗ CSV export failed: {e}")
            return False
    
    @staticmethod
    def export_to_pdf(data: List[Dict], filename: str, title: str = "E-Rate Data Report",
                     ai_analysis: Optional[str] = None, question: Optional[str] = None) -> bool:
        """
        Export data to formatted PDF report
        
        Args:
            data: List of records
            filename: Output filename
            title: Report title
            ai_analysis: Optional AI analysis text to include
            question: Optional question that was asked
            
        Returns:
            True if successful
        """
        if not data:
            print("✗ No data to export")
            return False
        
        try:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#1a5490'),
                spaceAfter=12
            )
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Metadata
            story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Paragraph(f"<b>Total Records:</b> {len(data)}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # AI Analysis Section (if provided)
            if ai_analysis and question:
                story.append(Paragraph("AI Analysis", styles['Heading2']))
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph(f"<b>Question:</b> {question}", styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
                
                # Format AI response
                analysis_lines = ai_analysis.split('\n')
                for line in analysis_lines:
                    if line.strip():
                        if line.startswith('#'):
                            story.append(Paragraph(line.replace('#', '').strip(), styles['Heading3']))
                        else:
                            story.append(Paragraph(line, styles['Normal']))
                
                story.append(PageBreak())
            
            # Summary Statistics
            story.append(Paragraph("Summary Statistics", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            stats = DataExporter._calculate_stats(data)
            for key, value in stats.items():
                story.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal']))
            
            story.append(Spacer(1, 0.3*inch))
            
            # Data Table (first 50 records)
            story.append(Paragraph("Data Records (showing first 50)", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            table_data = [['Organization', 'State', 'Status', 'Funding Requested']]
            for record in data[:50]:
                org = record.get('organization_name', 'N/A')[:40]
                state = record.get('state', 'N/A')
                status = record.get('form_471_frn_status_name', 'N/A')[:20]
                funding = f"${float(record.get('funding_commitment_request', 0) or 0):,.0f}"
                table_data.append([org, state, status, funding])
            
            table = Table(table_data, colWidths=[3*inch, 0.6*inch, 1.5*inch, 1.2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            story.append(table)
            
            if len(data) > 50:
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph(f"<i>... and {len(data) - 50} more records. Export to CSV for complete data.</i>", styles['Italic']))
            
            doc.build(story)
            print(f"✓ Exported PDF report to {filename}")
            return True
            
        except Exception as e:
            print(f"✗ PDF export failed: {e}")
            return False
    
    @staticmethod
    def _calculate_stats(data: List[Dict]) -> Dict[str, str]:
        """Calculate summary statistics"""
        total = len(data)
        
        # Status counts
        statuses = {}
        for record in data:
            status = record.get('form_471_frn_status_name', 'Unknown')
            statuses[status] = statuses.get(status, 0) + 1
        
        # Funding totals
        total_funding = sum(
            float(record.get('funding_commitment_request', 0) or 0)
            for record in data
        )
        
        # States
        states = set(record.get('state', '') for record in data if record.get('state'))
        
        return {
            "Total Applications": f"{total:,}",
            "Unique States": len(states),
            "Total Funding Requested": f"${total_funding:,.2f}",
            "Most Common Status": max(statuses.items(), key=lambda x: x[1])[0] if statuses else "N/A",
        }
