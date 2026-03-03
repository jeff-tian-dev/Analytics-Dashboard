import { Flex, Button, Text } from "@radix-ui/themes";
import { ChevronLeftIcon, ChevronRightIcon } from "@radix-ui/react-icons";

interface Props {
  page: number;
  pageSize: number;
  total: number;
  onChange: (page: number) => void;
}

export function Pagination({ page, pageSize, total, onChange }: Props) {
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  if (totalPages <= 1) return null;

  return (
    <Flex align="center" justify="center" gap="3" pt="4">
      <Button
        variant="soft"
        size="2"
        disabled={page <= 1}
        onClick={() => onChange(page - 1)}
      >
        <ChevronLeftIcon /> Prev
      </Button>
      <Text size="2" color="gray">
        Page {page} of {totalPages}
      </Text>
      <Button
        variant="soft"
        size="2"
        disabled={page >= totalPages}
        onClick={() => onChange(page + 1)}
      >
        Next <ChevronRightIcon />
      </Button>
    </Flex>
  );
}
