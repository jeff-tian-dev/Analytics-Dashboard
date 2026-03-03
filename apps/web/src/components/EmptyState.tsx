import { Flex, Text } from "@radix-ui/themes";
import { InfoCircledIcon } from "@radix-ui/react-icons";

export function EmptyState({ message = "No data found." }: { message?: string }) {
  return (
    <Flex align="center" justify="center" direction="column" py="9" gap="2">
      <InfoCircledIcon width={32} height={32} color="var(--gray-8)" />
      <Text size="3" color="gray">
        {message}
      </Text>
    </Flex>
  );
}
