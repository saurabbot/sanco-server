"""insert initial services data

Revision ID: 27f43f40fecc
Revises: becc7e6faeba
Create Date: 2026-01-15 04:29:33.840485

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27f43f40fecc'
down_revision: Union[str, None] = 'becc7e6faeba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    services_data = [
        {
            'name': 'Grease Trap Cleaning & Maintenance',
            'description': 'Professional grease trap cleaning and maintenance services to ensure optimal performance and compliance with health regulations.',
            'short_description': 'Professional grease trap cleaning and maintenance',
            'long_description': 'Our comprehensive grease trap cleaning and maintenance service ensures your commercial kitchen operates efficiently and complies with all health and safety regulations. We provide thorough cleaning, inspection, and maintenance to prevent blockages and maintain optimal performance.',
        },
        {
            'name': 'Grease Trap Supply & Installation',
            'description': 'Complete grease trap supply and installation services for new and existing commercial kitchens.',
            'short_description': 'Grease trap supply and installation',
            'long_description': 'We offer a full range of grease trap solutions including supply of high-quality units and professional installation services. Our team ensures proper sizing, correct placement, and compliance with local building codes and regulations.',
        },
        {
            'name': 'Grease Trap Treatment (Bacteria Block & Chemical Supply)',
            'description': 'Biological and chemical treatment solutions to maintain grease trap efficiency and prevent odors.',
            'short_description': 'Grease trap treatment and chemical supply',
            'long_description': 'Our grease trap treatment service includes bacteria blocks and specialized chemicals that break down grease and organic matter, preventing clogs and eliminating odors. Regular treatment extends the life of your grease trap and reduces maintenance frequency.',
        },
        {
            'name': 'Kitchen Exhaust Duct Cleaning & Maintenance',
            'description': 'Thorough cleaning and maintenance of kitchen exhaust systems to ensure fire safety and optimal ventilation.',
            'short_description': 'Kitchen exhaust duct cleaning',
            'long_description': 'Professional kitchen exhaust duct cleaning removes built-up grease and debris that pose fire hazards. Our comprehensive service includes cleaning of hoods, ducts, fans, and filters, ensuring compliance with fire safety regulations and optimal kitchen ventilation.',
        },
        {
            'name': 'Water Tank Cleaning & Chlorination',
            'description': 'Professional water tank cleaning and chlorination services to ensure clean and safe water supply.',
            'short_description': 'Water tank cleaning and chlorination',
            'long_description': 'Regular water tank cleaning and chlorination is essential for maintaining water quality and preventing contamination. Our service includes thorough cleaning, disinfection, and chlorination to ensure your water supply meets health standards.',
        },
        {
            'name': 'Sewage Tank & Sump Pit Cleaning',
            'description': 'Complete cleaning and maintenance of sewage tanks and sump pits to prevent overflow and maintain proper drainage.',
            'short_description': 'Sewage tank and sump pit cleaning',
            'long_description': 'Our sewage tank and sump pit cleaning service removes accumulated waste, sludge, and debris to prevent blockages and overflow. We ensure proper disposal of waste in compliance with environmental regulations.',
        },
        {
            'name': 'Tanker Service (1000/5000/10,000 gallon capacity)',
            'description': 'Reliable tanker services with multiple capacity options for waste collection and transportation.',
            'short_description': 'Tanker service with multiple capacities',
            'long_description': 'We provide tanker services with capacities of 1000, 5000, and 10,000 gallons for efficient waste collection and transportation. Our fleet is well-maintained and operated by experienced professionals to ensure reliable and timely service.',
        },
        {
            'name': 'High-Pressure Drain Line Jetting (Pipeline Block Removal)',
            'description': 'Advanced high-pressure jetting technology to remove stubborn blockages from drain lines and pipelines.',
            'short_description': 'High-pressure drain line jetting',
            'long_description': 'Our high-pressure drain line jetting service uses powerful water jets to break through tough blockages, tree roots, and accumulated debris in pipelines. This non-invasive method effectively clears blockages without damaging pipes, restoring proper drainage flow.',
        },
        {
            'name': 'Cooking Waste Oil Collection',
            'description': 'Eco-friendly collection and disposal of used cooking oil from commercial kitchens.',
            'short_description': 'Cooking waste oil collection',
            'long_description': 'We provide responsible collection and recycling of used cooking oil from commercial kitchens. Our service helps reduce environmental impact while ensuring proper disposal in compliance with regulations. Collected oil is processed for recycling into biodiesel and other products.',
        },
    ]
    
    def escape_sql_string(value):
        if value is None:
            return 'NULL'
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    
    for service in services_data:
        name = escape_sql_string(service['name'])
        description = escape_sql_string(service.get('description'))
        short_description = escape_sql_string(service.get('short_description'))
        long_description = escape_sql_string(service.get('long_description'))
        
        op.execute(f"""
            INSERT INTO services (name, description, short_description, long_description, created_at, updated_at)
            VALUES ({name}, {description}, {short_description}, {long_description}, NOW(), NOW())
        """)


def downgrade() -> None:
    service_names = [
        'Grease Trap Cleaning & Maintenance',
        'Grease Trap Supply & Installation',
        'Grease Trap Treatment (Bacteria Block & Chemical Supply)',
        'Kitchen Exhaust Duct Cleaning & Maintenance',
        'Water Tank Cleaning & Chlorination',
        'Sewage Tank & Sump Pit Cleaning',
        'Tanker Service (1000/5000/10,000 gallon capacity)',
        'High-Pressure Drain Line Jetting (Pipeline Block Removal)',
        'Cooking Waste Oil Collection',
    ]
    
    for name in service_names:
        escaped_name = name.replace("'", "''")
        op.execute(f"DELETE FROM services WHERE name = '{escaped_name}'")
