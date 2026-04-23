package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.Listing;
import com.nusacarbon.api.entity.enums.ListingStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ListingRepository extends JpaRepository<Listing, Integer> {
    List<Listing> findByStatusListing(ListingStatus status);
    List<Listing> findBySellerIdUser(Integer userId);
    List<Listing> findByStatusListingAndProjectKategoriNamaKategoriIgnoreCase(
            ListingStatus status, String namaKategori);
}
