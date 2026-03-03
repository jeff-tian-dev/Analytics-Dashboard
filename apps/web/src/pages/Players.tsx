import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { Box, Heading, Table, TextField } from "@radix-ui/themes";
import { MagnifyingGlassIcon } from "@radix-ui/react-icons";
import { api, Player } from "../lib/api";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { EmptyState } from "../components/EmptyState";
import { Pagination } from "../components/Pagination";

export function Players() {
  const [searchParams, setSearchParams] = useSearchParams();
  const page = Number(searchParams.get("page") || "1");
  const search = searchParams.get("search") || "";

  const [players, setPlayers] = useState<Player[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [searchInput, setSearchInput] = useState(search);

  useEffect(() => {
    setLoading(true);
    const params: Record<string, string> = { page: String(page), page_size: "20" };
    if (search) params.search = search;

    api.players(params)
      .then((res) => {
        setPlayers(res.data);
        setTotal(res.total);
      })
      .finally(() => setLoading(false));
  }, [page, search]);

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    setSearchParams(searchInput ? { search: searchInput, page: "1" } : {});
  }

  return (
    <Box>
      <Heading size="6" mb="4">
        Players
      </Heading>

      <form onSubmit={handleSearch} className="mb-4 max-w-sm">
        <TextField.Root
          placeholder="Search by name..."
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
        >
          <TextField.Slot>
            <MagnifyingGlassIcon />
          </TextField.Slot>
        </TextField.Root>
      </form>

      {loading ? (
        <LoadingSpinner />
      ) : players.length === 0 ? (
        <EmptyState message="No players found." />
      ) : (
        <>
          <Table.Root variant="surface">
            <Table.Header>
              <Table.Row>
                <Table.ColumnHeaderCell>Name</Table.ColumnHeaderCell>
                <Table.ColumnHeaderCell>TH</Table.ColumnHeaderCell>
                <Table.ColumnHeaderCell>Trophies</Table.ColumnHeaderCell>
                <Table.ColumnHeaderCell>War Stars</Table.ColumnHeaderCell>
                <Table.ColumnHeaderCell>Role</Table.ColumnHeaderCell>
                <Table.ColumnHeaderCell>League</Table.ColumnHeaderCell>
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {players.map((p) => (
                <Table.Row key={p.tag}>
                  <Table.Cell>
                    <Link
                      to={`/players/${encodeURIComponent(p.tag)}`}
                      className="text-[var(--accent-11)] hover:underline font-medium"
                    >
                      {p.name}
                    </Link>
                  </Table.Cell>
                  <Table.Cell>{p.town_hall_level}</Table.Cell>
                  <Table.Cell>{p.trophies.toLocaleString()}</Table.Cell>
                  <Table.Cell>{p.war_stars}</Table.Cell>
                  <Table.Cell>{p.role || "—"}</Table.Cell>
                  <Table.Cell>{p.league_name || "—"}</Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table.Root>
          <Pagination
            page={page}
            pageSize={20}
            total={total}
            onChange={(p) => {
              const next: Record<string, string> = { page: String(p) };
              if (search) next.search = search;
              setSearchParams(next);
            }}
          />
        </>
      )}
    </Box>
  );
}
