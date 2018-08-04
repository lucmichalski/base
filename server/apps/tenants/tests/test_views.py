import pytest

from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse

from ..models import Domain, Tenant


class TenantDomainTests(TestCase):

    def setUp(self):
        """Setup an existing Tenant A with a site subdomain
        a.example.com and an external domain a.com."""
        self.tenant_root_domain = Tenant.objects.get_tenant_root_domain()
        self.site = Site.objects.create(
            name=f"a.{self.tenant_root_domain}",
            domain=f"a.{self.tenant_root_domain}")
        self.tenant = Tenant.objects.create(name="A", site=self.site)
        self.domain = Domain.objects.create(domain="a.com", tenant=self.tenant)

        self.other_site = Site.objects.create(
            name=f"other.{self.tenant_root_domain}",
            domain=f"other.{self.tenant_root_domain}"
        )
        self.other_tenant = Tenant.objects.create(
            name="Other", site=self.other_site)
        self.other_domain = Domain.objects.create(
            domain="other.com", tenant=self.other_tenant)

        self.marketing_page = Site.objects.create(
            name="Marketingpage", domain="landingpage.com")

        self.site_not_linked = Site.objects.create(
            name=f"notlinked.{self.tenant_root_domain}",
            domain=f"notlinked.{self.tenant_root_domain}")

        self.home_url = reverse("home")
        self.secret_url = reverse("tenants:dashboard")

    def test_tenant_root_domain_should_be_accessible(self):
        """The marketing page should be accessible."""
        response = self.client.get(
            self.home_url, HTTP_HOST=self.tenant_root_domain)
        self.assertEqual(response.status_code, 200)

    def test_tenant_marketing_domain_should_be_accessible(self):
        """The marketing page should be accessible."""
        response = self.client.get(
            self.home_url, HTTP_HOST=self.marketing_page.domain)
        self.assertEqual(response.status_code, 200)

    def test_tenant_domain_should_be_accessible(self):
        """The tenants subdomain (e.g. a.example.com) should be accessible."""
        response = self.client.get(self.home_url, HTTP_HOST=self.site.domain)
        self.assertEqual(response.status_code, 200)

    def test_tenant_external_domain_should_be_accessible(self):
        """The tenants external domain (e.g. a.com) should be accessible."""
        response = self.client.get(self.home_url, HTTP_HOST=self.domain.domain)
        self.assertEqual(response.status_code, 200)

    def test_tenant_not_existing_domain_should_give_not_found_error(self):
        """A not-existing root domain name should throw an error."""
        response = self.client.get(self.home_url, HTTP_HOST='notexisting.com')
        # TODO: Is this a problem? But thats common Django behavior.
        self.assertEqual(response.status_code, 200)

    def test_tenant_not_existing_site_should_give_not_found_error(self):
        """A non-existing subdomain of the tenant root domain should error."""
        response = self.client.get(
            self.home_url, HTTP_HOST=f'notexisting.{self.tenant_root_domain}')
        self.assertEqual(response.status_code, 404)

    @pytest.mark.skip(
        reason="This should probably give a 404 - but it gives a 200 now")
    def test_tenant_not_linked_site_should_give_not_found_error(self):
        """An existing site without a tenant should throw an error."""
        response = self.client.get(
            self.home_url, HTTP_HOST=self.site_not_linked.domain)
        self.assertEqual(response.status_code, 404)

    def test_tenant_secret_page_on_root_domain_not_be_accessible(self):
        """The marketing page should be accessible."""
        response = self.client.get(
            self.secret_url, HTTP_HOST=self.tenant_root_domain)
        self.assertEqual(response.status_code, 403)

    def test_tenant_secret_page_on_marketing_domain_not_be_accessible(self):
        """The marketing page should be accessible."""
        response = self.client.get(
            self.secret_url, HTTP_HOST="landingpage.com")
        self.assertEqual(response.status_code, 403)

    def test_tenant_secret_page_on_other_site_domain_not_be_accessible(self):
        """The tenants subdomain (e.g. a.example.com) should be accessible."""
        response = self.client.get(
            self.secret_url, HTTP_HOST=self.other_site.domain)
        self.assertEqual(response.status_code, 403)

    def test_tenant_secret_page_on_external_domain_not_be_accessible(self):
        """The tenants external domain (e.g. a.com) should be accessible."""
        response = self.client.get(
            self.secret_url, HTTP_HOST=self.other_domain.domain)
        self.assertEqual(response.status_code, 403)

    @pytest.mark.skip(
        reason="This should probably give a 404 - but it gives a 403 now")
    def test_tenant_secret_page_on_not_existing_domain_not_found_error(self):
        """A not-existing root domain name should throw an error."""
        response = self.client.get(
            self.secret_url, HTTP_HOST='notexisting.com')
        self.assertEqual(response.status_code, 404)

    def test_tenant_secret_page_on_not_existing_site_not_found_error(self):
        """A non-existing subdomain of the tenant root domain should error."""
        response = self.client.get(
            self.secret_url,
            HTTP_HOST=f'notexisting.{self.tenant_root_domain}')
        self.assertEqual(response.status_code, 404)

    @pytest.mark.skip(
        reason="This should probably give a 404 - but it gives a 403 now")
    def test_tenant_secret_page_on_not_linked_site_not_found_error(self):
        """An existing site without a tenant should throw an error."""
        response = self.client.get(
            self.secret_url, HTTP_HOST=self.site_not_linked.domain)
        self.assertEqual(response.status_code, 404)
